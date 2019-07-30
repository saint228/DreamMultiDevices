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
                            imgSrc = PNG["PNGAddress"][event.point.x];
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
                valueSuffix: 'fps',
            },
            legend: commonLegend,
            series: [
                {
                    name: '运行帧数',
                    data: FPS["FPS"],
                    events: {
                        click: function(event) {
                            imgSrc = PNG["PNGAddress"][event.point.x];
                            htmlStr = "<img onclick='clickpng(this)' src='" + imgSrc + "'>";
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

        var flag = true;//状态true为正常的状态,false为放大的状态
        function clickpng(obj){
      //图片点击事件
       imgH = obj.height; //获取图片的高度
       imgW = obj.width; //获取图片的宽度
       if(flag){
           //图片为正常状态,设置图片宽高为现在宽高的2倍
           flag = false;//把状态设为放大状态
           obj.height = imgH*2;
           obj.width = imgW*2;
       }else{
           //图片为放大状态,设置图片宽高为现在宽高的二分之一
           flag = true;//把状态设为正常状态
           obj.height = imgH/2;
           obj.width = imgW/2;
       }
 
   }

    });
</script>