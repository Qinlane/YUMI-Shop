$(function () {
	// 导航左侧栏js效果 start
	$(".pullDownList li").hover(function () {
		$(".yMenuListCon").fadeIn();
		var index = $(this).index(".pullDownList li");
		if (!($(this).hasClass("menulihover") || $(this).hasClass("menuliselected"))) {
			$($(".yBannerList")[index]).css("display", "block").siblings().css("display", "none");
			$($(".yBannerList")[index]).removeClass("ybannerExposure");
			setTimeout(function () {
				$($(".yBannerList")[index]).addClass("ybannerExposure");
			}, 60)
		} else {}
		$(this).addClass("menulihover").siblings().removeClass("menulihover");
		$(this).addClass("menuliselected").siblings().removeClass("menuliselected");
		$($(".yMenuListConin")[index]).fadeIn().siblings().fadeOut();
	}, function () {

	})
	$(".pullDown").mouseleave(function () {
		$(".yMenuListCon").fadeOut();
		$(".yMenuListConin").fadeOut();
		$(".pullDownList li").removeClass("menulihover");

	})
	// 导航左侧栏js效果  end

})


/*公共部分---------------------------------------------------*/
//制保留2位小数，如：2，会在2后面补上00.即2.00 
function toDecimal2(x) {
	var f = parseFloat(x);
	if (isNaN(f)) {
		return false;
	}
	var f = Math.round(x * 100) / 100;
	var s = f.toString();
	var rs = s.indexOf('.');
	if (rs < 0) {
		rs = s.length;
		s += '.';
	}
	while (s.length <= rs + 2) {
		s += '0';
	}
	return s;
}

// 公共返回顶部
function backTop() {
	$(window).scroll(function () {
		var dTop = $(document).scrollTop();
		var fTop = $('.layout-header .navbar').height();
		if (dTop > fTop) {
			$('.layout-magnet').show();
		} else {
			$('.layout-magnet').hide();
		}
	});
	$(".layout-magnet").click(function () {
		$("html").animate({
			"scrollTop": "0px"
		}, 500); //IE,FF
		$("body").animate({
			"scrollTop": "0px"
		}, 500); //Webkit
	});
}