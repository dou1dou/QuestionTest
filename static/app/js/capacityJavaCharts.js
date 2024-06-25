let java_value, python_value, c_value;

$(document).ready(function (){
    $.ajax({
        url: "/get_solved_various_number/api/",
        method: "GET",
        success: function(response){
            const homework_progress = $(".various_chart_capacity");
            java_value = response['java'];
            python_value = response['python'];
            c_value = response['c'];

        const chart_capacity = echarts.init(
            document.getElementById('chart_capacity'), 'white', {renderer: 'canvas'});
        const option_capacity = {
    "backgroundColor": "#ffffff",
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
            "type": "radar",
            "name": "\u505a\u9898\u6b63\u786e\u7387",
            "data": [
                [
                    java_value,
                    python_value,
                    c_value
                ]
            ],
            "label": {
                "show": false,
                "margin": 8
            },
            "itemStyle": {
                "normal": {}
            },
            "lineStyle": {
                "show": true,
                "width": 1,
                "opacity": 1,
                "curveness": 0,
                "type": "solid",
                "color": "#CD0000"
            },
            "areaStyle": {
                "opacity": 0
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
                "\u505a\u9898\u6b63\u786e\u7387"
            ],
            "selected": {},
            "left": "36%",
            "top": "80%"
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
    "radar": [
        {
            "indicator": [
                {
                    "name": "java",
                    "max": 1
                },
                {
                    "name": "python",
                    "max": 1
                },
                {
                    "name": "c",
                    "max": 1
                }
            ],
            "startAngle": 90,
            "name": {
                "textStyle": {
                    "color": "#999999"
                }
            },
            "splitLine": {
                "show": true,
                "lineStyle": {
                    "show": true,
                    "width": 1,
                    "opacity": 1,
                    "curveness": 0,
                    "type": "solid"
                }
            },
            "splitArea": {
                "show": true,
                "areaStyle": {
                    "opacity": 1
                }
            },
            "axisLine": {
                "show": true,
                "onZero": true,
                "onZeroAxisIndex": 0
            }
        }
    ]
};
        chart_capacity.setOption(option_capacity);
        },

        error: function (){
            alert("请求失败！")
        }
    });
})
