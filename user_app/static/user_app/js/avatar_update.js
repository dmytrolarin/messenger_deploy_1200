$(document).ready(function(){
    $('#formUpdateAvatar').on('submit', function(event){
        event.preventDefault()
        let formData = new FormData(this)
        $.ajax({
            type: 'post',
            data: formData,
            url: this.action,
            contentType: false,
            processData: false
        })
    })
})