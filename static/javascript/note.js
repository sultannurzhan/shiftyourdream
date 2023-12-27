//Create Note Function ------------------------------------------------------------------------------------------------
$('.note-form').submit(function(event) {
    event.preventDefault();  // Prevent the default form submission

    var noteForm = $(this);
    var title = noteForm.find('#title').val();
    var body = noteForm.find('#body').val();
    var userId = noteForm.data('user-id');
    var csrfToken = noteForm.find('input[name=csrfmiddlewaretoken]').val();
    var homeUrl = noteForm.data('home-url');
    var important = noteForm.find('#important').prop('checked');  // Check if the checkbox is checked

    

    $.ajax({
        url: 'create_note/',
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

                    // Remove the deleted note from the DOM
                    $("#" + formId).closest('.wrapper').remove();
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
    $(".delete-note-btn").click(function() {
        var formId = $(this).closest('form').attr('id');
        $("#confirmDeleteBtn").data('form-id', formId);
    });
});

//--------------------------------------------------------------------------------------------------------------------




//Edit Note Function -------------------------------------------------------------------------------------------------
$(document).ready(function () {
    // Function to update the modal content
    function updateEditNoteModal(noteId) {
        // Use Ajax to fetch the note details
        $.ajax({
            url: `/get_note_details/${noteId}/`,  // Update the URL to fetch note details
            method: 'GET',
            success: function (data) {
                // Update the modal content with note details
                $('#editNote .modal-title').text('Edit Dream');
                $('#editNote form').attr('action', `/edit_note/${noteId}/`);  // Update the form action
                $('#editNote #editTitle').val(data.title);
                $('#editNote #editBody').val(data.body);

                // Set the state of the "important" checkbox
                var importantCheckbox = $('#editNote #editImportant');
                importantCheckbox.prop('checked', data.important);
            },
            error: function (error) {
                console.error('Error fetching note details:', error);
            }
        });
    }

    // Event listener for the edit note buttons
    $('.edit-note-btn').on('click', function () {
        var noteId = $(this).data('note-id');
        updateEditNoteModal(noteId);
    });
});

//--------------------------------------------------------------------------------------------------------------------