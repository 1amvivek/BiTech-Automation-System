/**
 * Created by lvivek on 8/23/17.
 */
           function removeId(id) {
               if($("#"+id).css("text-decoration-line") == "none") {
                   $("#"+id).css("text-decoration", "line-through");
                   $("#"+id).css('color', 'red');
                   $("#input"+id).remove();

               } else {
                   $("#"+id).css("text-decoration", "none");
                   $("#"+id).css('color', 'inherit');
                   $('<input type="text" />').attr({
                       id: 'input'+id, value: id, style: 'display:none'
                }).appendTo("#"+id);

               }
           }




