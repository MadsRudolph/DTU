// Run from repository root. Output is committed; users do not need Node/npm to install.
const fs=require('node:fs'),path=require('node:path'),{execFileSync}=require('node:child_process');
const dir=path.resolve(__dirname,'../Obsidian/.obsidian/plugins/hypersketch');
fs.writeFileSync(path.join(dir,'geometry-source.js'),'module.exports='+JSON.stringify(fs.readFileSync(path.join(dir,'geometry.js'),'utf8'))+';\n');
const icons={};for(const size of [192,512])icons[`icon-${size}.png`]=fs.readFileSync(path.join(dir,`icon-${size}.png`)).toString('base64');
fs.writeFileSync(path.join(dir,'icons-base64.js'),'module.exports='+JSON.stringify(icons)+';\n');
execFileSync('npx',['--yes','esbuild@0.25.12',path.join(dir,'plugin.js'),'--bundle','--platform=node','--format=cjs','--target=es2022','--external:obsidian','--outfile='+path.join(dir,'main.js')],{stdio:'inherit'});

const output=path.join(dir,'main.js');fs.writeFileSync(output,fs.readFileSync(output,'utf8').replace(/[ \t]+$/gm,''));
