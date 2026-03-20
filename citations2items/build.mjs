async function buildBootstrapScript(opts: ReportingOptions) {
  const { logLevel } = opts;
  return await esbuild({
    entryPoints: [
      './bootstrap.tsx',
    ],
    absWorkingDir: join(PACKAGE_ROOT, '..', 'anafero-gui'),
    entryNames: '[dir]/[name]',
    assetNames: '[dir]/[name]',
    format: 'iife',
    target: ['esnext'],
    bundle: true,
    minify: false,
    treeShaking: true,
    sourcemap: true,
    platform: 'browser',
    outfile: join(PACKAGE_ROOT, 'bootstrap.js'),
    //outdir: 'layout',
    write: true,
    loader: {
      '.module.css': 'local-css',
      '.css': 'css',
      // '.jpg': 'file',
      // '.png': 'file',
    },
    logLevel,
    plugins: [{
      name: 'lunr-patch',
      setup(build) {
        build.onLoad({ filter: /lunr\.js$/ }, async (args) => {
          let contents = await readFile(args.path, 'utf8');
          contents = contents.replace(
            'if (global.console && console.warn)',
            'if (window.console && console.warn)',
          );
          return { contents, loader: 'js' };
        });
      },
    }],
  });
}

