<svelte:options accessors={true} />

<script lang="ts">
	import type { Gradio, SelectData } from "@gradio/utils";
	import { tick } from 'svelte'
	import File from "./shared/File.svelte";
	import Markdown from "./shared/Markdown.svelte";
	import type { FileData } from "@gradio/client";
	import { Block, BlockLabel } from "@gradio/atoms";
	import * as pdfjsLib from "pdfjs-dist";
	pdfjsLib.GlobalWorkerOptions.workerSrc = 'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.worker.min.js';

	import { StatusTracker } from "@gradio/statustracker";
	import type { LoadingStatus } from "@gradio/statustracker";

	export let elem_id = "";
	export let elem_classes: string[] = [];
	export let visible = true;
	export let value: null | FileData | FileData[];
	export let n: number = 0;
	export let files_with_original_ext: string[];
	export let interface_language: string = "fr";

	export let interactive: boolean = false;
	export let root: string;
	export let label: string = null;
	export let show_label: boolean = false;
	export let height: string | undefined;

	export let _selectable = false;
	export let loading_status: LoadingStatus;
	export let container = true;
	export let scale: number | null = null;
	export let min_width: number | undefined = undefined;
	export let gradio: Gradio<{
		change: never;
		error: string;
		upload: never;
		clear: never;
		select: SelectData;
		clear_status: LoadingStatus;
		delete: FileData;
	}>;

	let file: FileData;
	let old_file: null | FileData = null;

	let renderTasks = [];
	let blinking;
	let viewer;

	const htmlFormats = ['.html', '.svg'];
	const imageFormats = ['.png', '.jpg', '.jpeg'];
	const markdownFormats = ['.md', '.txt'];
	const codeFormats = ['.py', '.js', '.css', '.json', '.yaml', '.yml', '.xml', '.sh', '.bash', '.log', '.ts', '.tsx', '.js', '.jsx', '.cpp'];

	if (Array.isArray(value)) {
		file = value[n];
	} else {
		file = value;
	}
	
	$: if (value && (JSON.stringify(old_file) !== JSON.stringify(value[n]))) {
		console.log(`value ${value}`)
		gradio.dispatch("change");
		old_file = value[n];
		file = add_url(value[n], root);
		if (file) {
			if (file.path.endsWith('pdf')) {
				show_pdf(file);
			} else if (htmlFormats.some(ext => file.path.endsWith(ext))) {
				console.log("HTML");
				show_html(file);
			} else if (imageFormats.some(ext => file.path.endsWith(ext))) {
				console.log("Image");
				show_image(file);
			} else if (markdownFormats.some(ext => file.path.endsWith(ext)) || codeFormats.some(ext => file.path.endsWith(ext))) {
				console.log("Markdown");
				show_markdown(file);
			} else {
				console.log("Autre");
				show_error();
			}
		}
	}

	function add_url(file, root) {
			console.log("Add url en cours");
			console.log(root);
			console.log(file);
			if (file) {
				file.url = root + "/file=" + file.path
			}
			return file
		}

    async function show_error() {
        await tick(); // Attend la fin du rendu
        viewer.innerHTML = '';

        const errorMessage = interface_language.startsWith('fr')
            ? 'Format non pris en charge'
            : 'Unsupported format';

        viewer.innerHTML = `<div class="error-message">${errorMessage}</div>`;
    }

	async function show_pdf(file) {
		console.log("Get doc en cours");
		await tick(); // Attend la fin du rendu
		viewer.innerHTML = '';
		blinking.style.display = 'block';
		const loadingTask = pdfjsLib.getDocument(file.url);
		const pdfDoc = await loadingTask.promise;
		console.log('PDF loaded');
		
		const fragment = document.createDocumentFragment(); // Crée un fragment de document

		const renderPage = async (pageNum) => {
			const page = await pdfDoc.getPage(pageNum);
			console.log(`Page ${pageNum} loaded`);
			const scale = 1.5;
			const viewport = page.getViewport({ scale: scale });

			// Création d'un nouveau canevas pour chaque page
			const canvas = document.createElement('canvas');
			canvas.height = viewport.height;
			canvas.width = viewport.width;
			fragment.appendChild(canvas); // Ajoute le canevas au fragment

			const context = canvas.getContext('2d');

			// Rendu de la page
			const renderContext = {
				canvasContext: context,
				viewport: viewport
			};
			const renderTask = page.render(renderContext);
			renderTasks.push(renderTask); // Ajoute la tâche de rendu à la liste
			await renderTask.promise;
			console.log(`Page ${pageNum} rendered`);
		};

		// Parallélisation du chargement et du rendu des pages
		const renderPromises = [];
		for (let pageNum = 1; pageNum <= pdfDoc.numPages; pageNum++) {
			renderPromises.push(renderPage(pageNum));
		}
		await Promise.all(renderPromises);

		viewer.appendChild(fragment); // Ajoute le fragment au conteneur
		blinking.style.display = 'none';
	}

	async function show_html(file) {
		await tick(); // Attend la fin du rendu
		viewer.innerHTML = ''; // Vide le conteneur
		blinking.style.display = 'block';

        try {
            const response = await fetch(file.url);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const htmlContent = await response.text();

            const iframe = document.createElement('iframe');
            iframe.style.width = '100%';
            iframe.style.height = '100%';
            iframe.srcdoc = htmlContent; // Utilise le contenu HTML comme source de l'iframe

			viewer.appendChild(iframe); // Ajoute l'iframe au conteneur
        } catch (error) {
            console.error('Error fetching HTML content:', error);
        }
		blinking.style.display = 'none';
    }

	async function show_image(file) {
		await tick(); // Attend la fin du rendu
		viewer.innerHTML = ''; // Vide le conteneur
		blinking.style.display = 'block';

		try {
			const response = await fetch(file.url);
			if (!response.ok) {
				throw new Error(`HTTP error! status: ${response.status}`);
			}
			const blob = await response.blob();
			const imageUrl = URL.createObjectURL(blob);

			const img = document.createElement('img');
			img.style.width = '100%';
			img.src = imageUrl; // Utilise l'URL de l'image comme source de l'élément img
			viewer.appendChild(img); // Ajoute l'image au conteneur
		} catch (error) {
			console.error('Error fetching image content:', error);
		}
		blinking.style.display = 'none';
	}

	async function show_markdown(file) {
		await tick(); // Attend la fin du rendu
		viewer.innerHTML = ''; // Vide le conteneur
		blinking.style.display = 'block';

		try {
			const response = await fetch(file.url);
			if (!response.ok) {
				throw new Error(`HTTP error! status: ${response.status}`);
			}
			let markdownContent = await response.text();

			// Vérifie l'extension du fichier
			const extensionMatch = file.path.match(/\.(\w+)$/);
        	if (extensionMatch) {
            	const extension = extensionMatch[1];
			console.log(extension);
            if (codeFormats.includes(`.${extension}`)) {
                markdownContent = `\`\`\`${extension}\n${markdownContent}\n\`\`\``;
            }
        }
			// Crée dynamiquement un composant Svelte
			new Markdown({
				target: viewer,
				props: {
					value: markdownContent,
				}
			});
		} catch (error) {
			console.error('Error fetching Markdown content:', error);
		}
		blinking.style.display = 'none';
	}

	async function next_file() {
		await tick(); // Attend la fin du rendu
		blinking.style.display = 'none';
		renderTasks.forEach(task => task.cancel());
		renderTasks = [];
		console.log("Bouton cliqué !");
		n = (n + 1) % value.length;
 	}

	async function previous_file() {
		await tick(); // Attend la fin du rendu
		blinking.style.display = 'none';
		renderTasks.forEach(task => task.cancel());
		renderTasks = [];
		console.log("Bouton cliqué !");
		n = (n - 1 + value.length) % value.length;
		console.log(n);
 	}

</script>

<Block {visible} {elem_id} {elem_classes} {container} {scale} {min_width} {height}>
    {#if loading_status}
        <StatusTracker
            autoscroll={gradio.autoscroll}
            i18n={gradio.i18n}
            {...loading_status}
        />
    {/if}
    <BlockLabel
        show_label={false}
        Icon={File}
        float={1}
        label={null}
    />
    {#if file}
		<div class="viewer-container">
			<div bind:this={blinking} class="viewer-blinker" style="display: none">
				<span>·</span><span>·</span><span>·</span>
			</div>
			<div bind:this={viewer} class="viewer"></div>
			<div class="button-row">
				{#if Array.isArray(value) && value.length > 1}
					<button class="next-button" on:click={previous_file}>
						<svg width="18" height="18" viewBox="0 0 18 18" xmlns="http://www.w3.org/2000/svg">
							<polygon points="12.4,3.8 5.6,9 12.4,14.2" fill="none" stroke_width="1.5" stroke_linejoin="round" stroke_linecap="round" />
						</svg>
					</button>
				{/if}
				<span class="file-name">&nbsp;&nbsp;&nbsp;{files_with_original_ext[n]}&nbsp;&nbsp;&nbsp;</span>
				{#if Array.isArray(value) && value.length > 1}
					<button class="next-button" on:click={next_file}>
						<svg width="18" height="18" viewBox="0 0 18 18" xmlns="http://www.w3.org/2000/svg">
							<polygon points="5.6,3.8 12.4,9 5.6,14.2" fill="none" stroke_width="1.5" stroke_linejoin="round" stroke_linecap="round" />
						</svg>
					</button>
				{/if}
			</div>
		</div>
	{/if}
	<style>
		:root {
            --neo-blue: rgb(0, 162, 223);
			--neo-white: rgb(255, 255, 255);
			--neo-black: rgb(5, 5, 5);
		}
		.viewer-container {
			position: relative;
			overflow: hidden;
			height: 100%;
			width: 100%;
			display: flex;
			flex-direction: column;
		}
		.viewer {
			display: flex;
			flex-direction: column;
			width: 100%;
			height: 100%;
			overflow: auto;
		}
		.error-message {
			text-align: center;
		}
		.viewer canvas {
			margin: .1vh 0;
		}
		.button-row {
			display: flex;
			flex-direction: row;
			width: 100%;
			justify-content: center;
			align-items: center;
		}
		.file-name {
			max-width: 90%;
			overflow: hidden;
			text-overflow: ellipsis;
			white-space: nowrap;
		}
		.viewer-blinker {
			position: absolute;
			top: 50%;
			left: 50%;
			transform: translate(-50%, -50%);
			color: var(--neo-blue);
			animation: blinker 1.5s cubic-bezier(.5, 0, 1, 1) infinite alternate;
			font-size: 3em;
		}
		.viewer-blinker span {
			opacity: 0;
			animation-name: blinker;
			animation-duration: 1.5s;
			animation-timing-function: cubic-bezier(.5, 0, 1, 1);
			animation-iteration-count: infinite;
		}
		.viewer-blinker span:nth-child(1) {
			animation-delay: 0s;
		}
		.viewer-blinker span:nth-child(2) {
			animation-delay: .5s; /* Délai pour le deuxième point */
		}
		.viewer-blinker span:nth-child(3) {
			animation-delay: 1s; /* Délai pour le troisième point */
		}
		@keyframes blinker {  
            0%, 100% { opacity: 0; }
            50% { opacity: 1; }
        }
		/* Style par défaut */
		.next-button polygon {
		stroke: var(--neo-black);
		}
		.dark .next-button polygon {
		stroke: var(--neo-white);
		}
	</style>
</Block>
