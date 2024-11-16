<script>
	import { page } from '$app/stores';


	const tag = $derived($page.url.searchParams.get('tag'));
	const tab = $derived($page.url.searchParams.get('tab') ?? 'all');
</script>

<svelte:head>
	<title>Movease</title>
</svelte:head>

<div class="home-page">
	<div class="container page">
		<h1>
			Welcome to Movease
		</h1>
		<a href="/incidents" class="btn btn-lg btn-primary">
			Incidents
		</a>
	</div>
</div>
