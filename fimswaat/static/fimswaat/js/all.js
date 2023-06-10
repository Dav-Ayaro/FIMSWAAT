document.getElementById("myButton").addEventListener("click", function() {
    var loader = document.getElementById("loader");
    loader.style.display = "block";
    
    // Simulate some asynchronous task (e.g., fetching data)
    setTimeout(function() {
        loader.style.display = "none";
      // Perform the desired action after the loader is hidden
      // e.g., navigate to a new page or load content dynamically
    }, 2000); // Replace 2000 with the desired time for the asynchronous task
    });
