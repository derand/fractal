Mandelbrot Fractal Image Generator
===

Script generate set of fractal images. [Demo](http://www.youtube.com/watch?v=W05GIITJ7pU)

To convert images to video file use:

    ffmpeg -y -f image2 -i ./mandelbrot_%04d.jpg -an -vcodec libx264 -crf 18 -refs 4 -threads 2 -partitions +parti4x4+parti8x8+partp4x4+partp8x8+partb8x8 -subq 12 -trellis 1 -coder 1 -me_range 32 -level 4.1 -profile:v high -bf 12 -r 23.976  ./mandelbrot.mp4

or animated gif:

    convert -delay 20 -loop 0 ./mandelbrot_* ./mandelbrot.gif

