function alert_message(message_icon,message_title)
{
    Swal.fire(
    {
        confirmButtonColor:'#a6c4f1',
        icon: message_icon,
        title: message_title,
          //text: 'Something went wrong!',:
    }
    )
}
