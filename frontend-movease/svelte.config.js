import adapter from "@sveltejs/adapter-static";

export default {
	kit: {
		adapter: adapter({
			pages: "build",
			assets: "build",
			fallback: "app.html",
			precompress: false,
			strict: false,
		}),
	},
};