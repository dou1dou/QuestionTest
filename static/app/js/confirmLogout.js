function confirmLogout() {
    const userConfirmed = confirm("确定要注销账号吗？");
    if (userConfirmed) {
        // 在这里添加实际的注销账号逻辑，例如发送请求到服务器
        alert("账号已注销");
        // 示例：重定向到首页
        window.location.href = "/";
    } else {
        alert("已取消注销");
    }
}