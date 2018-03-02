/**
 * Created by luoranbin on 2017/12/18.
 */
function select_change() {
    var objs = document.getElementById("option_type")
    var get_value = objs.options[objs.selectedIndex].value;
    return get_value
}