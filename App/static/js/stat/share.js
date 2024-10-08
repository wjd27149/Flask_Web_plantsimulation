// 折线图2
// 绘制图表
// 1. 实例化对象
var lineChart2 = echarts.init(document.querySelector("#container"));
// 2.指定配置
var lineOption2 = {
    tooltip: {
        trigger: "axis"
    },
    grid: {
        left: "4%",
    },
    legend: {
        data:["日分享情况"],
        textStyle: {
            color: "#4c9bfd"
        },
    },
    xAxis: {
        type: 'category',
        data: [],
        axisTick: {
            show: false // 去除刻度线
        },
        axisLabel: {
            color: "#4c9bfd" // 文本颜色
        },
        axisLine: {
            show: false // 去除轴线
        }
    },
    yAxis: {
      type: 'value',
      axisTick: {
            show: false // 去除刻度线
        },
      axisLabel: {
            color: "#4c9bfd" // 文本颜色
        },
      axisLine: {
            show: false // 去除轴线
        },
    },
    series: [
      {
        name:"日分享情况",
        data: [],
        type: 'line',
        smooth: true,
        // 设置拐点
        symbol: "circle",
        // 拐点大小
        symbolSize: 5,
        // 开始不显示拐点，鼠标经过显示
        showSymbol: false,
        // 设置拐点颜色以及边框
        itemStyle: {
            borderColor: "rgba(221, 220, 107, .1)",
            borderWidth: 8
        },
      }
    ]
};

// 3. 把配置给实例对象
lineChart2.setOption(lineOption2);
// 4. 让图表跟随屏幕自动的去适应
window.addEventListener("resize", function() {
    lineChart2.resize();
});

//折线图2数据获取
function getLineData2(){
    $.ajax({
        url: "/chart/share",
        type:"POST",
        success: function(res) {
            lineOption2.xAxis.data=res.data.categories;
            lineOption2.series[0].data=res.data.series.share;
            lineChart2.setOption(lineOption2);
        },
        error: function(xhr, type, errorThrown) {

        }
    })
};
getLineData2();