//Create Dream Function ------------------------------------------------------------------------------------------------
$('.dream-form').submit(function(event) {
    event.preventDefault();  // Prevent the default form submission

    var dreamForm = $(this);
    var title = dreamForm.find('#title').val();
    var body = dreamForm.find('#body').val();
    var userId = dreamForm.data('user-id');
    var csrfToken = dreamForm.find('input[name=csrfmiddlewaretoken]').val();
    var homeUrl = dreamForm.data('home-url');
    var important = dreamForm.find('#important').prop('checked');  // Check if the checkbox is checked

    

    $.ajax({
        url: 'create_dream/',
        type: 'POST',
        data: {
            'csrfmiddlewaretoken': csrfToken,
            'title': title,
            'body': body,
            'user_id': userId,
            'important': important.toString(),  // Convert to string for consistent handling
        },
        success: function(data) {
            //alert(important)
            // Handle success, so redirect to 'home'
            window.location.href = homeUrl;
        },
        error: function(error) {
            console.error(error);
        }
    });
});

//----------------------------------------------------------------------------------------------------------------



//CHANGE THE BODY FIELD FUNCTION --------------------------------------------------------------------------------
$(function() {
    $('[id^="bodyfield-"]').each(function() {
        var bodyfield = $(this);
        var title = bodyfield.data('title');

        if (title.length == 0) {
            // Change the style of bodyfield 
            bodyfield.css('max-height', '180px');
        } 
    });
});
//----------------------------------------------------------------------------------------------------------------



//DELETE FUNCTION ----------------------------------------------------------------------------------------------------
$(document).ready(function() {
    $("#confirmDeleteBtn").click(function() {
        // Get the form ID from the modal's data attribute
        var formId = $(this).data('form-id');

        // Close the modal
        $("#confirmDeleteModal").modal("hide");

        // Send the AJAX request
        $.ajax({
            url: $("#" + formId).attr("action"),
            type: "POST",
            data: $("#" + formId).serialize(),
            success: function(response) {
                if (response.success) {
                    // Optional: Do something on success, e.g., show a success message
                    console.log(response.success);
 
                    // Remove the deleted dream from the DOM
                    $("#" + formId).closest('.my-wrapper').remove();
                } else {
                    // Optional: Do something on failure, e.g., show an error message
                    console.log(response.error);
                }
            },
            error: function(xhr, textStatus, error) {
                // Optional: Handle the AJAX error
                console.log(error);
            }
        });
    });

    // Attach the form ID to the modal's delete button
    $(".delete-dream-btn").click(function() {
        var formId = $(this).closest('form').attr('id');
        $("#confirmDeleteBtn").data('form-id', formId);
    });
});

//--------------------------------------------------------------------------------------------------------------------




//Edit Dream Function -------------------------------------------------------------------------------------------------
$(document).ready(function () {
    // Function to update the modal content
    function updateEditDreamModal(dreamId) {
        // Use Ajax to fetch the dream details
        $.ajax({
            url: `/get_dream_details/${dreamId}/`,  // Update the URL to fetch dream details
            method: 'GET',
            success: function (data) {
                // Update the modal content with dream details
                $('#editDream .modal-title').text('Edit Dream');
                $('#editDream form').attr('action', `/edit_dream/${dreamId}/`);  // Update the form action
                $('#editDream #editTitle').val(data.title);
                $('#editDream #editBody').val(data.body);

                // Set the state of the "important" checkbox
                var importantCheckbox = $('#editDream #editImportant');
                importantCheckbox.prop('checked', data.important);
            },
            error: function (error) {
                console.error('Error fetching dream details:', error);
            }
        });
    }

    // Event listener for the edit dream buttons
    $('.edit-dream-btn').on('click', function () {
        var dreamId = $(this).data('dream-id');
        updateEditDreamModal(dreamId);
    });
});

//--------------------------------------------------------------------------------------------------------------------
