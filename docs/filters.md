## Image Processing Filters

### Resizing Operations

#### Fit to Rectangle

```
w(WIDTH)h(HEIGHT)
```
* **WIDTH** — rectangle width in pixels
* **HEIGHT** — rectangle height in pixels

When aspect ratios do not match, the image is resized to fit the largest side of the rectangle.

#### Fill Rectangle

```
w(WIDTH)h(HEIGHT)fill
```
* **WIDTH** — rectangle width in pixels
* **HEIGHT** — rectangle height in pixels

When aspect ratios do not match, the image is resized to fit the smallest side, and parts outside the rectangle are cropped.

#### Resize with Conversion

```
w(WIDTH)h(HEIGHT)(fit|fill).(FORMAT)
```
* **WIDTH** — rectangle width in pixels
* **HEIGHT** — rectangle height in pixels
* **fit|fill** — optional rectangle filling mode
* **FORMAT** — target conversion format

### Color Manipulation (Raster Images Only)

#### Saturation Adjustment

```
sat(SATURATION)
```
* **SATURATION** — percentage value to increase or decrease saturation

#### Brightness Adjustment

```
bright(BRIGHTNESS)
```
* **BRIGHTNESS** — percentage value to increase or decrease brightness

#### Blur Effect

```
blur(RADIUSxSIGMA)
```
* **RADIUS** — blur operator radius
* **SIGMA** — blur operator sigma value

### Watermark Overlay

```
wm
```

* Watermark overlay parameters are defined in the **settings.py** configuration file

### Format Conversion

```
c.(FORMAT)
```
* **FORMAT** — target image format for conversion

**Supported vector image conversions:**
* PNG
* PDF
* PS
* SVG
* XML