---
title: Frontend CSS Snippets & Patterns
description: Frontend CSS Snippets & Patterns.
---

## Styling

### Element centering
```css
/* center-align div */
div {
  width:300px;
  margin:auto;
}

/* Center Vertically - Using padding */
.center {
  padding: 70px 0;
  border: 3px solid green;
  text-align: center;
}

/* Center Vertically - Using line-height */
.center {
  line-height: 200px;
  height: 200px;
  border: 3px solid green;
  text-align: center;
}

/* If the text has multiple lines, add the following: */
.center p {
  line-height: 1.5;
  display: inline-block;
  vertical-align: middle;
}

/* Center Vertically - Using position & transform */
.center {
  height: 200px;
  position: relative;
  border: 3px solid green;
}

.center p {
  margin: 0;
  position: absolute;
  top: 50%;
  left: 50%;
  -ms-transform: translate(-50%, -50%);
  transform: translate(-50%, -50%);
}

/* Center Vertically - Using Flexbox */

.center {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 200px;
  border: 3px solid green;
}
```

### Align elements side by side

```css
/* float */
div.mycontainer {
  width:100%;
  overflow:auto;
}
div.mycontainer div {
  width:33%;
  float:left;
}

/* inline-block */
div {
  width: 30%;
  display: inline-block;
}

/* flex */
.mycontainer {
  display: flex;
}
.mycontainer > div {
  width:33%;
}

/* grid */
.grid-container {
  display: grid;
  grid-template-columns: 33% 33% 33%;
}

/* A more modern way of creating column layouts, is to use CSS Flexbox, but not support < IE10 */
/* Content layout with IE6-10 supprot */
/* Create three equal columns that float next to each other */
.column {
  float: left;
  width: 33.33%;
}

/* Clear floats after the columns */
.row:after {
  content: "";
  display: table;
  clear: both;
}

/* Responsive layout - makes the three columns stack on top of each other instead of next to each other on smaller screens (600px wide or less) */
@media screen and (max-width: 600px) {
  .column {
    width: 100%;
  }
}
```

### Background
```css
/* multiple background images */
#example1 {
  background-image: url(img_flwr.gif), url(paper.gif);
  background-position: right bottom, left top;
  background-repeat: no-repeat, repeat;
  padding: 15px;
}

/* Full Size Background Image */
html {
  background: url(img_man.jpg) no-repeat center fixed;
  background-size: cover;
}

/* text in background image */
.hero-image {
  background: url(img_man.jpg) no-repeat center;
  background-size: cover;
  height: 500px;
  position: relative;
}

.hero-text {
  text-align: center;
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  color: white;
}

/*
<div class="hero-image">
  <div class="hero-text">
    <h1 style="font-size:50px">I am John Doe</h1>
    <h3>And I'm a Photographer</h3>
    <button>Hire me</button>
  </div>
</div>
*/
```

### Image

```css
/* responsive image */
img {
  max-width: 100%;
  height: auto;
}

/* center image */

/* Using margin: auto */
img {
  display: block;
  margin: auto;
  width: 50%;
}

/* Using display: flex */
div {
  display: flex;
  justify-content: center;
}

img {
  width: 50%;
}

/* Center an Image Vertically */
div {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 600px;
  border: 1px solid black;
}

img {
  width: 50%;
  height: 50%;
}
```

### Miscellaneous
- If you do not want to apply opacity to child elements, use RGBA color values instead of opacity

## JavaScript
- Placing scripts at the bottom of the <body> element improves the display speed, because script interpretation slows down the display.

- Cached JavaScript files can speed up page loads.
