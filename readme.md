## About

This project aims to automatically determine the stats and IVs of a Pokemon given only a single screenshot. This way, the IVs can be computed easily, without any private information. Notably, it accurately detects the level of the Pokemon given your trainer level, which narrows down the IV range significantly.

The real timesink is, unfortunately, taking screenshots of every one of your Pokemon. On my iPhone, that takes roughly one minute per 20 Pokemon. It's faster than keying data into an overlay or a text file, but it still takes some time.

Currently, it only works with the iPhone 6S Plus because that's the only phone I have at the moment. Resizing screenshots to the iPhone size (width 1242 pixels) should work, but I haven't tested that at all. It should be portable to other devices with some minor tweaks - let me know if you have clean screenshots for other screen sizes.

## Taking Screenshots

There's a bit of subtlety here. The CP number up top and the little level meter "ball" on the level arc must both be clearly visible. Some Pokemon, particularly the flying ones, might obscure one or both, which will cause recognition failures. To avoid this, you can rotate the Pokemon (drag left/right on the top area), or make it "roar" (tap on it) to make it change posture and possibly make the screenshot easier to take.

Some Pokemon, like Scyther, move around too much to make screenshotting reliable; you may want to key in information manually for these.
