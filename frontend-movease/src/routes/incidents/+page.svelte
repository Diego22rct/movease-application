<script>
	import { page } from "$app/stores";
	import { onMount } from "svelte";

	import { writable } from "svelte/store";

	let incidents = writable([]);

	const tag = $derived($page.url.searchParams.get("tag"));
	const tab = $derived($page.url.searchParams.get("tab") ?? "all");

	const obtenerIncidencias = async () => {
		const response = await fetch("http://localhost:8000/api/v1/incidents/");
			incidents.set(await response.json());
		if (response.ok) {
			incidents = await response.json();
			console.log(incidents);
		} else {
			alert("Error al obtener incidencias");
		}
	};
	onMount(obtenerIncidencias);
</script>

<svelte:head>
	<title>Movease</title>
</svelte:head>
<div class="container">
	{#if $incidents.length > 0}
		<ul>
			{#each $incidents as incident}
				<li>
					<h3>{incident.title}</h3>
					<p>{incident.description}</p>
					<p><strong>Estado:</strong> {incident.status}</p>
					<p><strong>Creada el:</strong> {incident.created_at}</p>
				</li>
			{/each}
		</ul>
	{:else}
		<p>No hay incidencias registradas.</p>
	{/if}
</div>

<style>
	.container {
		max-width: 800px;
		margin: 0 auto;
	}

	ul {
		list-style-type: none;
		padding: 0;
	}

	li {
		margin: 1rem 0;
		padding: 1rem;
		border: 1px solid #ccc;
	}

	h3 {
		margin: 0;
		font-size: 1.25rem;
	}

	p {
		margin: 0.5rem 0;
	}
</style>
