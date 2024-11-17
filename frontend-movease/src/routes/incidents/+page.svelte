<script>
	import { onMount } from "svelte";
	import { writable } from "svelte/store";

	const incidents = writable([]);

	const obtenerIncidencias = async () => {
		const response = await fetch("http://localhost:8000/api/v1/incidents/");
		if (response.ok) {
			const incidentData = await response.json();

			for (const incident of incidentData) {
				if (incident.images && Array.isArray(incident.images)) {
					incident.imageUrls = incident.images.map(
						(base64Str) => `data:image/png;base64,${base64Str}`, // Ajusta el tipo MIME según sea necesario (image/png, image/jpeg, etc.)
					);
				}
			}

			incidents.set(incidentData);
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
					{#if incident.imageUrls && incident.imageUrls.length > 0}
						<strong>Imágenes:</strong>
						<div>
							{#each incident.imageUrls as imageUrl}
								<img src={imageUrl} alt="Imagen del incidente" />
							{/each}
						</div>
					{/if}
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

	img {
		max-width: 100%;
		height: auto;
		margin-top: 1rem;
	}
</style>
