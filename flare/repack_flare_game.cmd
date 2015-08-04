@echo off

SET game_dir=..\..\flare-game
SET mods=fantasycore,alpha_demo
SET spritesheetpacker_args=--save-always

call repack.cmd
