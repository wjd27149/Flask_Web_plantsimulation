// 折线图1
// 绘制图表
// 1. 实例化对象
var lineChart1 = echarts.init(document.querySelector("#member_order"));
// 2.指定配置
var lineOption1 = {
    // 通过这个color修改两条线的颜色
    color: ["#00f2f1","#ed3f35"],
    tooltip: {
        trigger: "axis"
    },
    legend: {
        // 如果series 对象有name 值，则 legend可以不用写data
        // 修改图例组件 文字颜色
        textStyle: {
            color: "#4c9bfd"
        },
    },

    xAxis: {
        type: "category",
        boundaryGap: false,
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
        type: "value",
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
    series: [{
            name: "订单总数",
            type: "line",
            // true 可以让我们的折线显示带有弧度
            smooth: true,
           // 设置拐点
            symbol: "circle",
            // 拐点大小
            symbolSize: 5,
            // 开始不显示拐点， 鼠标经过显示
            showSymbol: false,
            // 设置拐点颜色以及边框
            itemStyle: {
                borderColor: "rgba(221, 220, 107, .1)",
                borderWidth: 8
            },
            data: []
        },
        {
            name: "会员总数",
            type: "line",
            smooth: true,
            // 设置拐点
            symbol: "circle",
            // 拐点大小
            symbolSize: 5,
            // 开始不显示拐点， 鼠标经过显示
            showSymbol: false,
            // 设置拐点颜色以及边框
            itemStyle: {
                borderColor: "rgba(221, 220, 107, .1)",
                borderWidth: 8
            },
            data: []
        }
    ]
};

// 3. 把配置给实例对象
lineChart1.setOption(lineOption1);
// 4. 让图表跟随屏幕自动的去适应
window.addEventListener("resize", function() {
    lineChart1.resize();
});

//折线图1数据获取
function getLineData1(){
    $.ajax({
        url: "/chart/dashboard",
        type:"POST",
        success: function(res) {
            lineOption1.xAxis.data=res.data.categories;
            lineOption1.series[0].data=res.data.series.orderSum;
            lineOption1.series[1].data=res.data.series.memberSum;
            lineChart1.setOption(lineOption1);
        },
        error: function(xhr, type, errorThrown) {

        }
    })
};
getLineData1();

// 折线图2
// 绘制图表
// 1. 实例化对象
var lineChart2 = echarts.init(document.querySelector("#finance"));
// 2.指定配置
var lineOption2 = {
    tooltip: {
        trigger: "axis"
    },
    legend: {
        data:["日营收情况"],
        textStyle: {
            color: "#4c9bfd"
        },
    },
    xAxis: {
        type: 'category',
        data: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
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
        name:"日营收情况",
        data: [820, 932, 901, 934, 1290, 1330, 1320],
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
        url: "/chart/finance",
        type:"POST",
        success: function(res) {
            lineOption2.xAxis.data=res.data.categories;
            lineOption2.series[0].data=res.data.series.finance;
            lineChart2.setOption(lineOption2);
        },
        error: function(xhr, type, errorThrown) {

        }
    })
};
getLineData2();