/* 
 * 初始化
*/

// 检测无障碍模式
auto.waitFor();
auto.setMode('fast');
// auto.setFlags('useShell');

// 获取、设置设备分辨率
const width = 1080;
const height = 2340;
setScreenMetrics(width, height);
// const width = device.width;
// const height = device.height;

// 获取用户名 & 密码用以登录
try{
    const {user} = hamibot.env;
    const {pass} = hamibot.env;
}catch{
    const user = null;
    const pass = null;
}

// const user = '';
// const pass = '';

// 控制台悬浮
// console.show();
// console.setSize(width / 2, height / 2);

// 自定义悬浮窗
setInterval(() => {}, 1000);
var w = floaty.window(
    <frame gravity='center' bg='#44ffcc00'>
        <text id='text'>悬浮窗</text>
    </frame>
);

// 悬浮窗窗口设置
w.setAdjustEnabled(false); // false -> 无法触摸 true -> 可触摸
// w.setTouchable(false);
w.setPosition(width / 14,  height % 2);
w.setSize(width / 3, height / 9); // -2, -2根据内容大小变化
// w.setSize(-2, -2);

// 悬浮窗内容
function floatWindow(textContent){
    ui.run(function() {
        w.text.setText(String(textContent));
    });
    console.log(textContent);
}
function exit(){
     if (w.exitOnClose()){
        console.verbose("用户关闭悬浮窗，停止执行脚本");
    }
}
exit();


// -------------------------------------------------------------------------------------------------

// 启动软件
if (app.getPackageName('com.zfsoft.jxtc') == false){
    console.error("设备未安装顶岗实习软件，请先安装！");
}else{
    app.launch('com.zfsoft.jxtc');
}
floatWindow("等待中……");

sleep(5000);

/*
 * 用户登录
*/
function login(button){
    floatWindow("需要登录，正尝试登陆中");
    try{
        setText(0, user);
        setText(1, pass);
        if (click('登 录')){
            floatWindow("登陆成功");
        }
    }catch{
        console.info("请先登录账号与密码，或将其配置在脚本处。");
        w.close();
        app.close;
        hamibot.exit();
    }

}

if (text('log_ic01').exists()){
    login();
}

/* 
 * 开始考勤
*/
function Click(button, text){
    if (button){
        sleep(2000);
        floatWindow("点击" + text);
        button.click();
    }
}

// while(!click('考勤'));
var work = text('考勤').findOne();
Click(work, "考勤");
sleep(3000);

// // swipe(width / 2, height * 2, width / 2, height * 2 - 550, 1000);
swipe(500, 1550, 500, 830, 2000);

var mark = text('备注').findOne();
setText("实习打卡");
click(width / 2, height / 2);

// var ra = new RootAutomator();

/*
 * 关闭
*/
floatWindow("已完成操作，5秒后关闭");
console.info("已完成操作，5秒后关闭");
sleep(1500);

for (var i = 5; i >= 1; i--){
    floatWindow(i);
    sleep(1000);
}

w.close();
app.close;
hamibot.exit();