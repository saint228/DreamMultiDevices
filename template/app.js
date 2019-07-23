<script src="../template/highcharts.js"></script>
<script type="text/javascript">
    var Time_series = // tag data

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
                categories: Time_series["Time"],
            },
            tooltip: {
                valueSuffix: '%',
            },
            legend: commonLegend,
            series: [
                {
                    name: '总CPU占比',
                    data: TotalCPU["TotalCPU"],
                    events: {
                        click: function(event) {
                            imgSrc = PNG["PNGAddress"][event.point.x];
                            htmlStr = "<img src='" + imgSrc + "'>";
                            $("#CpuScreen").html(htmlStr);
                        },
                    },
                }, 
                {
                    name: 'CPU占比',
                    data: AllocatedCPU["AllocatedCPU"],
                    events: {
                        click: function(event) {
                            imgSrc = PNG["PNGAddress"][event.point.x];
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
                categories: Time_series["Time"],
            },
            tooltip: {
                valueSuffix: 'MB',
            },
            legend: commonLegend,
            series: [
                {
                    name: '内存占用',
                    data: AllocatedMemory["AllocatedMemory(MB)"],
                    events: {
                        click: function(event) {
                            imgSrc = PNG["PNGAddress"][event.point.x];
                            htmlStr = "<img src='" + imgSrc + "'>";
                            $("#MemeryScreen").html(htmlStr);
                        },
                    },
                }, 
                {
                    name: '使用内存',
                    data: UsedMemory["UsedMemory(MB)"],
                    events: {
                        click: function(event) {
                            PNG["PNGAddress"][event.point.x];
                            htmlStr = "<img src='" + imgSrc + "'>";
                            $("#MemeryScreen").html(htmlStr);
                        },
                    },
                }, 
                {
                    name: '空闲内存',
                    data: FreeMemory["FreeMemory(MB)"],
                    events: {
                        click: function(event) {
                            imgSrc = PNG["PNGAddress"][event.point.x];
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
                 categories: Time_series["Time"],
            },
            tooltip: {
                valueSuffix: '%',
            },
            legend: commonLegend,
            series: [
                {
                    name: '运行帧数',
                    data: FPS["FPS"],
                    events: {
                        click: function(event) {
                            imgSrc = PNG["PNGAddress"][event.point.x];
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
                        "<td>" + data_count["Avg_AllocatedMemory"]+ "MB</td>" +
                        "<td>" + data_count["Max_AllocatedMemory"] + "MB</td>" +
                        "<td>" + data_count["Min_AllocatedMemory"]+ "MB</td>" +
                    "</tr>" +
                    "<tr>" +
                        "<td>CPU</td>" +
                        "<td>" + data_count["Avg_AllocatedCPU"] + "</td>" +
                        "<td>" + data_count["Max_AllocatedCPU"] + "</td>" +
                        "<td>" + data_count["Min_AllocatedCPU"] + "</td>" +
                    "</tr>" +
                    "<tr>" +
                        "<td>FPS</td>" +
                        "<td>" + data_count["Avg_FPS"]+ "</td>" +
                        "<td>" + data_count["Max_FPS"] + "</td>" +
                        "<td>" + data_count["Min_FPS"] + "</td>" +
                    "</tr>";
        $("#totalData").html(htmlStr);


    });
</script>