function submitData(mark_id) {
    // Get the modal
    var modal = document.getElementById("myModal");

    // Get the button that opens the modal
    var btn = document.getElementById("myBtn");

    // Get the <span> element that closes the modal
    var span = document.getElementsByClassName("close")[0];

    // When the user clicks the button, open the modal

     modal.style.display = "block";


    // When the user clicks on <span> (x), close the modal
    span.onclick = function() {
      modal.style.display = "none";
    }

    // When the user clicks anywhere outside of the modal, close it
    window.onclick = function(event) {
      if (event.target == modal) {
        modal.style.display = "none";
      }
    }
    // Handle form submission
    document.getElementById('myForm').addEventListener('submit', function(event) {
      event.preventDefault();

      var reason = document.getElementById('reason').value;
      var formData = new FormData();
      formData.append('reason', reason);
      formData.append('mark_id', mark_id); // Replace with actual mark_id


    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/remark', true);
    xhr.onreadystatechange = function() {
      if (xhr.readyState === 4 && xhr.status === 200) {
        // refesh the page
        setTimeout(function() {
        window.location.reload();
        }, 100);
      }
    };
    xhr.send(formData);

    modal.style.display = "none"; // Hide the modal after submission

    });

}


