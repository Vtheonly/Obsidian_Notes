The script won't work until the DOM tree is created. You cannot access properties of a null object.
Most of the time, people put the script tag at the bottom of the body tag.
You can also use the onload event even before creating the tree because the onload event waits until the element (window in this case) is loaded:

```javascript
window.onload = function () {
  document.querySelector("h1").style.color = "red";
}
```

document.write changes the whole structure of the HTML file. It replaces the original content with what you have in document.write.

It can also include HTML code because it replaces the original content.

Regarding your question about the most used methods in the window object, here's a more comprehensive list some of the most used methods in the window object are:

```javascript
window.onload()
window.alert()
window.close()
window.setTimeout()
window.setInterval()
window.clearTimeout()
window.clearInterval()
window.alert()
window.confirm()
window.prompt()
window.open()
window.close()
window.addEventListener()
window.removeEventListener()
window.scrollTo()
window.localStorage
window.sessionStorage
window.location
```

These methods are frequently used for various tasks such as timing, user interaction, window manipulation, and data storage in web development.