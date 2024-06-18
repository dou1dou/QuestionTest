let all, solved;

$(document).ready(function (){
    $.ajax({
        url: "/info/personal/get_solved_question_number/api/",
        method: "GET",
        success: function(response){
            const sum_solved = $(".circle-content1-sum");
            sum_solved.text(response['solved'] + "/" + response['all'])
            all = response['all'];
            solved = response['solved'];

            const chart_6002b0f3f7c74203bb5d1e2fc7983022 = echarts.init(
    document.getElementById('6002b0f3f7c74203bb5d1e2fc7983022'), 'white', {renderer: 'canvas'});
const option_6002b0f3f7c74203bb5d1e2fc7983022 = {
    "animation": true,
    "animationThreshold": 2000,
    "animationDuration": 1000,
    "animationEasing": "cubicOut",
    "animationDelay": 0,
    "animationDurationUpdate": 300,
    "animationEasingUpdate": "cubicOut",
    "animationDelayUpdate": 0,
    "aria": {
        "enabled": false
    },
    "color": [
        "#5470c6",
        "#91cc75",
        "#fac858",
        "#ee6666",
        "#73c0de",
        "#3ba272",
        "#fc8452",
        "#9a60b4",
        "#ea7ccc"
    ],
    "series": [
        {
            "type": "pie",
            "name": "\u5b8c\u6210\u5360\u6bd4",
            "colorBy": "data",
            "legendHoverLink": true,
            "selectedMode": false,
            "selectedOffset": 10,
            "clockwise": true,
            "startAngle": 90,
            "minAngle": 0,
            "minShowLabelAngle": 0,
            "avoidLabelOverlap": true,
            "stillShowZeroSum": true,
            "percentPrecision": 2,
            "showEmptyCircle": true,
            "emptyCircleStyle": {
                "color": "lightgray",
                "borderColor": "#000",
                "borderWidth": 0,
                "borderType": "solid",
                "borderDashOffset": 0,
                "borderCap": "butt",
                "borderJoin": "bevel",
                "borderMiterLimit": 10,
                "opacity": 1
            },
            "data": [
                {
                    "name": "\u603b\u9898\u91cf",
                    "value": all
                },
                {
                    "name": "\u5df2\u5b8c\u6210",
                    "value": solved
                }
            ],
            "radius": "35%",
            "center": [
                "50%",
                "50%"
            ],
            "label": {
                "show": false,
                "margin": 8
            },
            "labelLine": {
                "show": true,
                "showAbove": false,
                "length": 30,
                "length2": 30,
                "smooth": false,
                "minTurnAngle": 90,
                "maxSurfaceAngle": 90
            },
            "rippleEffect": {
                "show": true,
                "brushType": "stroke",
                "scale": 2.5,
                "period": 4
            }
        }
    ],
    "legend": [
        {
            "data": [
                "\u603b\u9898\u91cf",
                "\u5df2\u5b8c\u6210"
            ],
            "selected": {},
            "show": true,
            "left": "60%",
            "top": "70%",
            "orient": "vertical",
            "padding": 5,
            "itemGap": 10,
            "itemWidth": 25,
            "itemHeight": 14,
            "backgroundColor": "transparent",
            "borderColor": "#ccc",
            "borderRadius": 0,
            "pageButtonItemGap": 5,
            "pageButtonPosition": "end",
            "pageFormatter": "{current}/{total}",
            "pageIconColor": "#2f4554",
            "pageIconInactiveColor": "#aaa",
            "pageIconSize": 15,
            "animationDurationUpdate": 800,
            "selector": false,
            "selectorPosition": "auto",
            "selectorItemGap": 7,
            "selectorButtonGap": 10
        }
    ],
    "tooltip": {
        "show": true,
        "trigger": "item",
        "triggerOn": "mousemove|click",
        "axisPointer": {
            "type": "line"
        },
        "showContent": true,
        "alwaysShowContent": false,
        "showDelay": 0,
        "hideDelay": 100,
        "enterable": false,
        "confine": false,
        "appendToBody": false,
        "transitionDuration": 0.4,
        "textStyle": {
            "fontSize": 14
        },
        "borderWidth": 0,
        "padding": 5,
        "order": "seriesAsc"
    },
    "title": [
        {
            "show": true,
            "target": "blank",
            "subtarget": "blank",
            "left": "center",
            "top": "50",
            "padding": 5,
            "itemGap": 10,
            "textAlign": "auto",
            "textVerticalAlign": "auto",
            "triggerEvent": false
        }
    ]
};
        chart_6002b0f3f7c74203bb5d1e2fc7983022.setOption(option_6002b0f3f7c74203bb5d1e2fc7983022);
        },
        error: function (){
            alert("请求失败！")
        }
    });
})

