<script>
	import { page } from '$app/stores';
	import { goto } from '$app/navigation';


	const tag = $derived($page.url.searchParams.get('tag'));
	const tab = $derived($page.url.searchParams.get('tab') ?? 'all');

	import { writable } from 'svelte/store';

	const title = writable('');
	const description = writable('');
	const status = writable('open');  // Estado por defecto

	const agregarIncidencia = async () => {
		const response = await fetch("http://localhost:8000/api/v1/incidents", {
			method: "POST",
			headers: { "Content-Type": "application/json" },
			body: JSON.stringify({
				title: $title,
				description: $description,
				status: $status
			}),
		});

		if (response.ok) {
		alert('Incidencia agregada correctamente');
			goto('/incidents');  
		} else {
			alert('Error al agregar incidencia');
		}
	};
</script>

<svelte:head>
	<title>Movease - Nueva Incidencia</title>
</svelte:head>

<div class="container">
	<h1>Agregar Nueva Incidencia</h1>
	<form onsubmit={agregarIncidencia}>
		<label for="title">Título:</label>
		<input type="text" id="title" bind:value={$title} required />
		
		<label for="description">Descripción:</label>
		<textarea id="description" bind:value={$description} required></textarea>

		<label for="status">Estado:</label>
		<select id="status" bind:value={$status}>
		<option value="open">Abierta</option>
		<option value="closed">Cerrada</option>
		</select>

		<button type="submit">Agregar Incidencia</button>
	</form>
</div>
