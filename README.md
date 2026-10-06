# Rampart Nox

A Dragon's Dogma 2 recolour of the **Rampart Breaker** body armour (male): dark purple doublet, darker purple
knitted-leather vest and sleeves, purple shoulder caps and dark gold piping. Meshes, gloves, belts and cloth
physics stay vanilla; only material colours change.

Current version: **1.0**. Download it from [Releases](../../releases).

## Requirements

- [REFramework](https://www.nexusmods.com/dragonsdogma2/mods/8)
- [DD2MethodLibrary](https://www.nexusmods.com/dragonsdogma2/mods/1574) (REFramework plugin)
- Fluffy Mod Manager (the pak goes into `pak_mods`)

## Install

Add the release zip to Fluffy Mod Manager and enable it. Load your save and wear Rampart Breaker.
Don't combine it with other mods that change Rampart Breaker.

REFramework menu (Insert) > Script Generated UI > **Rampart Nox**: status, *Apply again*,
*Restore original colours* (switches back without uninstalling).

## How it works

The pak only **adds** files: two material files (copies of Rampart Breaker's with new colour values), two
recoloured knitted-leather pattern textures and two small skin prefabs. No vanilla file is replaced. The script
registers the new skins in the game's part catalogs under their own IDs and points Rampart Breaker's shirt and
sleeves at them. `build/` holds the Blender scripts that generate the files from the game's own data.

## Credits

- **Capcom** for Dragon's Dogma 2; the meshes, materials and textures this recolours are the game's own.
- Built with REFramework, RE Mesh Editor (ZZtaii fork), REE.PAK.Tool / ree-pak-cli and Blender.
- Made with the help of Claude (Anthropic).
