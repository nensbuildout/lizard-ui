function show_boxes() {
    $(".container-column li").each(function () {
        var link, url;
        link = $("a[href]", this);
        url = link.attr("href");
        console.log(url);
        if (!$(this).data("initialized")) {
            $(this).data("initialized", true);
            link.hide();
            $(this).load(url + " .box");
        };
    });
}


$(document).ready(function () {
    show_boxes();
});
