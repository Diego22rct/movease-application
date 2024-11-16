<script>
	import { page } from '$app/stores';
</script>

<nav class="navbar navbar-light">
	<div class="container">
		<a class="navbar-brand" href="/">Movease</a>
		<ul class="nav navbar-nav pull-xs-right">
			<li class="nav-item">
				<a class="nav-link" class:active={$page.url.pathname === '/incidents'} href="/incidents">Incidentes</a>
			</li>
			<li class="nav-item">
				<a class="nav-link" class:active={$page.url.pathname === '/new-incident'} href="/new-incident">Nuevo incidente</a>
			</li>
		</ul>
	</div>
</nav>
