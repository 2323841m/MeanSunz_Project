var infinite = new Waypoint.Infinite({
    element: $('.postBody')[0],
    onBeforePageLoad: function () {
        $('.load').show();
    },
    onAfterPageLoad: function ($items) {
        $('.load').hide();
    }
});
