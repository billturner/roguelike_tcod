# r/RoguelikeDev Does The Complete Roguelike Tutorial

![RoguelikeDev Does the Complete Roguelike Tutorial Event Logo](https://i.imgur.com/3MAzEp1.png)

At [r/roguelikedev](https://www.reddit.com/r/roguelikedev/) we're doing a dev-along following [The Complete Roguelike Tutorial](http://rogueliketutorials.com/tutorials/tcod/)

## Details on my game:

- This attempt is using the TCOD library
- Will complete the tutorial as close to the letter as possible, and then modify later

## If you would like to participate:

- Follow along with the [weekly posts](https://www.reddit.com/r/roguelikedev).
- Share your game on the final week.

## Notes & links:

- README based off of the one created by [Aaron Santos](https://gitlab.com/aaron-santos/roguelikedev-does-the-complete-roguelike-tutorial/tree/master)
- [TCOD API reference](https://python-tcod.readthedocs.io/en/latest/)

## Post tutorial goals:

- [x] Get rid of all deprecation notices
- [ ] Organize the codebase a bit more (all function utilities in one folder, etc)
  - [ ] move constants to own directory
- [ ] fix targeting and spell casting/canceling
- [ ] Fix dying, since right now you can just keep playing
  - [ ] set health to zero (can be negative)
  - [ ] don't allow movement
  - [ ] display some kind of message (fading in?)
- [ ] use a tileset
- [ ] have messages fading out at the top?
- [ ] Add type hinting throughout the app, validating with MyPy
- [ ] Create a common `colors` dictionary and use everywhere there are colors used
- [ ] After the above, maybe add ability to change "color themes"
