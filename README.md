# pygame-tutorial

## Notes:

### Display surface vs Surface:
The display surface is the main surface that we draw on and there can only be one and its always visible

A regular surface is an image of some kind, you can have any number but they are only visible when attached to the display surface


### importing images
convert() and convert_alpaha() are method to convert images to a preferible format for pygame. convert_alpaha() version is used if the image has transparent pixels. this can increase the performance

### movement
remember to always use delta time, otherwise movement speed will depend on frame rate

rect.center = direction * speed * dt