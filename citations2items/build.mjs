import { build as esbuild } from 'esbuild';
import { writeFile, readFile, mkdir, stat } from 'node:fs/promises';
import { basename } from 'node:path';


const appOut = 'build/dist';

const assets = [
  'build/compiled/bootstrap.js',
  'build/compiled/bootstrap.css',
  'index.html',
];


async function buildBootstrapScript() {

  await esbuild({
    entryPoints: [
      './bootstrap.tsx',
    ],
    entryNames: '[dir]/[name]',
    assetNames: '[dir]/[name]',
    format: 'esm',
    external: ['@riboseinc/paneron-registry-kit', '@riboseinc/paneron-extension-geodetic-registry'],
    target: ['esnext'],
    bundle: true,
    minify: false,
    treeShaking: true,
    sourcemap: true,
    platform: 'browser',
    outdir: 'build/compiled',
    //outfile: 'bootstrap.js',
    //outdir: 'layout',
    write: true,
    loader: {
      '.module.css': 'local-css',
      '.css': 'css',
      '.woff2': 'dataurl',
      '.ttf': 'dataurl',
      // '.jpg': 'file',
      // '.png': 'file',
    },
    logLevel: 'debug',
  });

  try {
    const appOutStat = await stat(appOut);
    if (!appOutStat.isDirectory()) {
      await mkdir(appOut);
    }
  } catch (e) {
    await mkdir(appOut);
  }

  async function copyAsset(path) {
    const filename = basename(path)
    const contents = await readFile(path);
    const outPath = `${appOut}/${filename}`;
    console.debug(`${path} -> ${outPath}`);
    await writeFile(outPath, contents);
  }

  for (const filePath of assets) {
    const mapFile = `${filePath}.map`;
    try {
      const mapStat = await stat(mapFile);
      if (mapStat.isFile()) {
        await copyAsset(mapFile);
      }
    } catch (e) {
    }
    await copyAsset(filePath);
  }

  // WHY?
  const bootstrapClientJS = `${appOut}/bootstrap.js`;
  const builtBootstrap =
    await readFile(bootstrapClientJS, { encoding: 'utf-8' });
  await writeFile(
    bootstrapClientJS,
    builtBootstrap.replace(
      '(import.meta.env ? import.meta.env.MODE : void 0) !== "production"',
      'false'),
    { encoding: 'utf-8' },
  );

}

await buildBootstrapScript();
