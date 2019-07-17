// 检查用户名
check_username: function() {
    var len = this.username.length;
    if (len < 5 || len > 20) {
        this.error_name_message = '请输入5-20个字符的昵称名';
        this.error_name = false;
    } else {
        this.error_name = false;
    }

    // 检查重名
    if (this.error_name == false) {
        axios.get(this.host + '/usernames/' + this.username + '/count/', {
                responseType: 'json'
            })
            .then(response => {
                if (response.data.count > 0) {
                    this.error_name_message = '用户名已存在';
                    this.error_name = true;
                } else {
                    this.error_name = false;
                }
            })
            .catch(error => {
                console.log(error.response.data);
            })
    }
}
