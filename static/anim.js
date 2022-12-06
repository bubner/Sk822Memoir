const all_elements = document.querySelectorAll("body");
const all_posts = document.querySelectorAll(".post");

// Fade in all HTML elements
for (let i = 0; i < all_elements.length; i++) {
    all_elements[i].style.display = "block";
    all_elements[i].style.animation = "fadeIn 0.75s";
}

// "Generate" the posts only in incrementing fashion
for (let i = 0, j = 1; i < all_posts.length; i++, j += 0.4) {
    all_posts[i].style.animation = "gen " + j + "s ease";
}