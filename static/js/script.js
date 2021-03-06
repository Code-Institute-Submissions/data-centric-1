/*-------Materialize jQuery------*/ 
$(document).ready(function(){
    $('.sidenav').sidenav();
    $(".dropdown-trigger").dropdown({ hover: false });
    $('.modal').modal();
    $('select').formSelect();
    $('#textarea1').val('');
    M.textareaAutoResize($('#textarea1'));

    // I copied the validateMaterializeSelect() function from Tims tutorial Task maneger videos
    // to make the validation work on the select from Materialize
    validateMaterializeSelect();
    function validateMaterializeSelect() {
        let classValid = { "border-bottom": "1px solid #4caf50", "box-shadow": "0 1px 0 0 #4caf50" };
        let classInvalid = { "border-bottom": "1px solid #f44336", "box-shadow": "0 1px 0 0 #f44336" };
        if ($("select.validate").prop("required")) {
            $("select.validate").css({ "display": "block", "height": "0", "padding": "0", "width": "0", "position": "absolute" });
        }
        $(".select-wrapper input.select-dropdown").on("focusin", function () {
            $(this).parent(".select-wrapper").on("change", function () {
                if ($(this).children("ul").children("li.selected:not(.disabled)").on("click", function () { })) {
                    $(this).children("input").css(classValid);
                }
            });
        }).on("click", function () {
            if ($(this).parent(".select-wrapper").children("ul").children("li.selected:not(.disabled)").css("background-color") === "rgba(0, 0, 0, 0.03)") {
                $(this).parent(".select-wrapper").children("input").css(classValid);
            } else {
                $(".select-wrapper input.select-dropdown").on("focusout", function () {
                    if ($(this).parent(".select-wrapper").children("select").prop("required")) {
                        if ($(this).css("border-bottom") != "1px solid rgb(76, 175, 80)") {
                            $(this).parent(".select-wrapper").children("input").css(classInvalid);
                        }
                    }
                });
            }
        });
    }
});

/*-------Email JS------*/ 
function sendEmail() {
    $("#message-sent").addClass("loader");
    emailjs.send("gmail", "template_TKAjL7PE", {
        from_name: document.querySelector("#first_name").value,
        from_email: document.querySelector("#email").value,
        message_html: document.querySelector("#textarea1").value,
    })
    .then(  
      function (response) { // "the .then, function(response/false) return false" code was used from the Resume project on the CI course.
        $("#message-sent").removeClass("loader").html(
            '<i class="fas fa-check"></i> Your message was sent Successfully!');
      },
      function (error) {
        $("#message-sent").removeClass("loader").css(
            "color", "#E91E63").html("Message Failed to send");
      }
    );
  return false; // To prevent the page from loading. 
}

//gets the close button
var close = document.querySelector(".grey.darken-1");

addEventListener("click", windowClick);

//clears the form when clicking the close button
function windowClick(e) {
    if (e.target == close) {
    $("#form")[0].reset();
    $(".clear").empty();
  }
}