<script>
import { page } from "$app/stores";
import { goto } from "$app/navigation";
import { writable } from "svelte/store";

const title = writable("");
const description = writable("");
const status = writable("open"); // Estado por defecto
let images = [];

const handleFileChange = (event) => {
	images = Array.from(event.target.files);
};

const agregarIncidencia = async (event) => {
	event.preventDefault(); 

	if (images.length === 0) {
		alert("Debe seleccionar al menos una imagen.");
		return;
	}

	if (images.length > 3) {
		alert("Solo se pueden subir un máximo de 3 imágenes.");
		return;
	}

	for (const image of images) {
		if (image.size > 5 * 1024 * 1024) {
			alert(
				"La imagen es demasiado grande. El tamaño máximo permitido es de 5MB.",
			);
			return;
		}

		if (!image.type.startsWith("image/")) {
			alert("El archivo seleccionado no es una imagen.");
			return;
		}
	}

	// Crear el objeto de incidencia
	const incident = {
		title: $title,
		description: $description,
		status: $status,
	};

	// Crear el objeto FormData
	const formData = new FormData();
	formData.append("title", $title);
	formData.append("description", $description);
	formData.append("status", $status);

	for (const image of images) {
		formData.append("images[]", image);
	}

	// Realizar la solicitud POST con el archivo
	try {
		const response = await fetch("http://localhost:8000/api/v1/incidents/upload", {
			method: "POST",
			body: formData,
		});

		if (response.ok) {
			alert("Incidencia agregada correctamente");
			goto("/incidents");
		} else {
			const errorData = await response.json();
			alert(`Error al agregar incidencia: ${errorData.error}`);
		}
	} catch (error) {
		alert(`Error al realizar la solicitud: ${error.message}`);
	}
};


</script>

<svelte:head>
    <title>Movease - Nueva Incidencia</title>
</svelte:head>

<div class="container">
    <h1>Agregar Nueva Incidencia</h1>
    <form on:submit={agregarIncidencia}>
        <label for="title">Título:</label>
        <input type="text" id="title" bind:value={$title} required />

        <label for="description">Descripción:</label>
        <textarea id="description" bind:value={$description} required></textarea>

        <label for="status">Estado:</label>
        <select id="status" bind:value={$status}>
            <option value="open">Abierta</option>
            <option value="closed">Cerrada</option>
        </select>

        <label for="images">Imágenes:</label>
        <input
            type="file"
            id="images"
            multiple
            accept="image/*"
            on:change={handleFileChange}
        />

        <button type="submit">Agregar Incidencia</button>
    </form>
</div>

<style>
    .container {
        max-width: 600px;
        margin: 0 auto;
        padding: 2rem;
        background-color: #f9f9f9;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }

    h1 {
        text-align: center;
        margin-bottom: 1.5rem;
    }

    form {
        display: flex;
        flex-direction: column;
    }

    label {
        margin-bottom: 0.5rem;
        font-weight: bold;
    }

    input,
    textarea,
    select {
        margin-bottom: 1rem;
        padding: 0.5rem;
        border: 1px solid #ccc;
        border-radius: 4px;
    }

    button {
        padding: 0.75rem;
        background-color: #007bff;
        color: white;
        border: none;
        border-radius: 4px;
        cursor: pointer;
        transition: background-color 0.3s;
    }

    button:hover {
        background-color: #0056b3;
    }
</style>