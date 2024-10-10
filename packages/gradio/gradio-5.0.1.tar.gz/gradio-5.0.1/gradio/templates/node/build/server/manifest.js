const manifest = (() => {
function __memo(fn) {
	let value;
	return () => value ??= (value = fn());
}

return {
	appDir: "_app",
	appPath: "_app",
	assets: new Set([]),
	mimeTypes: {},
	_: {
		client: {"start":"_app/immutable/entry/start.CJ7cI2d8.js","app":"_app/immutable/entry/app.Cid3sNNQ.js","imports":["_app/immutable/entry/start.CJ7cI2d8.js","_app/immutable/chunks/client.B3K4_ZU3.js","_app/immutable/entry/app.Cid3sNNQ.js","_app/immutable/chunks/preload-helper.DpQnamwV.js"],"stylesheets":[],"fonts":[],"uses_env_dynamic_public":false},
		nodes: [
			__memo(() => import('./chunks/0-oPczYPpW.js')),
			__memo(() => import('./chunks/1-D5QhYH7N.js')),
			__memo(() => import('./chunks/2-CClG50To.js').then(function (n) { return n.ax; }))
		],
		routes: [
			{
				id: "/[...catchall]",
				pattern: /^(?:\/(.*))?\/?$/,
				params: [{"name":"catchall","optional":false,"rest":true,"chained":true}],
				page: { layouts: [0,], errors: [1,], leaf: 2 },
				endpoint: null
			}
		],
		matchers: async () => {
			
			return {  };
		},
		server_assets: {}
	}
}
})();

const prerendered = new Set([]);

const base = "";

export { base, manifest, prerendered };
//# sourceMappingURL=manifest.js.map
