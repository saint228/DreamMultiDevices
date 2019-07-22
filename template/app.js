<script src="../template/highcharts.js"></script>
<script type="text/javascript">
    var data = // tag data
    
    function showFunction(obj) {
        $(".disableReport").removeClass("disableReport")
        $(obj).addClass("disableReport")
        $("#functionReport").show()
        $("#performanceReport").hide()
    }
    
    function showPerformance(obj) {
        $(".disableReport").removeClass("disableReport")
        $(obj).addClass("disableReport")
        $("#functionReport").hide()
        $("#performanceReport").show()
    }
    
    $(document).ready(function() {

        var commonTitle = {
            text: '',
        };
        var commonLegend = {
            layout: 'horizontal',
            align: 'center',
            verticalAlign: 'bottom',
        };
    
        var cpuData = {
            title: commonTitle,
            xAxis: {
                categories: data["YList"],
            },
            tooltip: {
                valueSuffix: '%',
            },
            legend: commonLegend,
            series: [
                {
                    name: '总CPU占比',
                    data: data["TotalCPU"],
                    events: {
                        click: function(event) {
                            imgSrc = data["ScreencapPNG"][event.point.x];
                            htmlStr = "<img src='" + imgSrc + "'>";
                            $("#CpuScreen").html(htmlStr);
                        },
                    },
                }, 
                {
                    name: 'CPU占比',
                    data: data["AllocatedCPU"],
                    events: {
                        click: function(event) {
                            imgSrc = data["ScreencapPNG"][event.point.x];
                            htmlStr = "<img src='" + imgSrc + "'>";
                            $("#CpuScreen").html(htmlStr);
                        },
                    },
                }, 
            ],
        };
        $('#CpuChart').highcharts(cpuData);
        
        var memeryData = {
            title: commonTitle,
            xAxis: {
                categories: data["YList"],
            },
            tooltip: {
                valueSuffix: 'MB',
            },
            legend: commonLegend,
            series: [
                {
                    name: '内存占用',
                    data: data["AllocatedMemory"],
                    events: {
                        click: function(event) {
                            imgSrc = data["ScreencapPNG"][event.point.x];
                            htmlStr = "<img src='" + imgSrc + "'>";
                            $("#MemeryScreen").html(htmlStr);
                        },
                    },
                }, 
                {
                    name: '使用内存',
                    data: data["UsedMemory"],
                    events: {
                        click: function(event) {
                            imgSrc = data["ScreencapPNG"][event.point.x];
                            htmlStr = "<img src='" + imgSrc + "'>";
                            $("#MemeryScreen").html(htmlStr);
                        },
                    },
                }, 
                {
                    name: '空闲内存',
                    data: data["FreeMemory"],
                    events: {
                        click: function(event) {
                            imgSrc = data["ScreencapPNG"][event.point.x];
                            htmlStr = "<img src='" + imgSrc + "'>";
                            $("#MemeryScreen").html(htmlStr);
                        },
                    },
                }, 
            ],
        };
        $('#MemeryChart').highcharts(memeryData);

        var FPSData = {
            title: commonTitle,
            xAxis: {
                categories: data["YList"],
            },
            tooltip: {
                valueSuffix: '',
            },
            legend: commonLegend,
            series: [
                {
                    name: '运行帧数',
                    data: data["AllocatedFPS"],
                    events: {
                        click: function(event) {
                            imgSrc = data["ScreencapPNG"][event.point.x];
                            htmlStr = "<img src='" + imgSrc + "'>";
                            $("#FPSScreen").html(htmlStr);
                        },
                    },
                },
            ],
        };
        $('#FPSChart').highcharts(FPSData);

        var htmlStr = "<tr>" +
                        "<td>内存</td>" +
                        "<td>" + data["StatisMemory"][0] + "MB</td>" +
                        "<td>" + data["StatisMemory"][1] + "MB</td>" +
                        "<td>" + data["StatisMemory"][2] + "MB</td>" +
                    "</tr>" +
                    "<tr>" +
                        "<td>CPU</td>" +
                        "<td>" + data["StatisCPU"][0] + "%</td>" +
                        "<td>" + data["StatisCPU"][1] + "%</td>" +
                        "<td>" + data["StatisCPU"][2] + "%</td>" +
                    "</tr>" +
                    "<tr>" +
                        "<td>FPS</td>" +
                        "<td>" + data["StatisFPS"][0] + "</td>" +
                        "<td>" + data["StatisFPS"][1] + "</td>" +
                        "<td>" + data["StatisFPS"][2] + "</td>" +
                    "</tr>";
        $("#totalData").html(htmlStr);

        for (var i = 1; i < data["FuncMemory"].length; i ++) {
            var htmlStr = data["FuncMemory"][i] + "MB / " + data["FuncCPU"][i] + "%";
            $("#detailBody #Func")[i - 1].append(htmlStr);
            var htmlStr2 = data["FuncFPS"][i];
            $("#detailBody #FuncFps")[i - 1].append(htmlStr2);
        }
    });
</script>