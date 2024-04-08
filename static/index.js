
  // function togglePopup() {
  //   var popup = document.getElementById("myPopup");
  //   // popup.classList.toggle("show");
  //   // var popup = document.querySelector('.popup');
  //   popup.classList.toggle("show");
  // }
// function togglePopup() {
//     var popup = document.querySelector('.popup');
//     popup.classList.toggle("show");
//   }
//   document.getElementById("feedbackForm").addEventListener("submit", function(event) {
//     event.preventDefault(); // 阻止默认的表单提交行为
//     togglePopup(); // 显示弹出框
//     // 在这里可以添加其他提交表单的逻辑
//   });
  function showDialogAndRedirect() {
    // 弹出对话框
    alert("Submitted! Back to homepage");

    // 设置定时器，以便在用户关闭对话框后跳转到其他页面
    setTimeout(function(){
      var form = document.getElementById('Feedbackform'); // 设置表单的提交方法为POST
      form.action = '/feedback'; // 提交表单 
      form.submit(); }, 500); // 延迟500毫秒跳转
    }

//for instructor to read feedback
    let currentqpage = 1;
    const qpages = document.querySelectorAll('.qpage');
  
    // current page
    function showqpage(qpageNumber) {
      qpages.forEach(qpage => {
        qpage.style.display = 'none'; // hide all page
      });
      document.getElementById(`qpage${qpageNumber}`).style.display = 'block'; // current page
  
    // last page
    function prevqpage() {
      if (currentqpage > 1) {
        currentqpage--;
        showqpage(currentqpage);
      }
    }
  
    // 下一页
    function nextqpage() {
      if (currentqpage < qpages.length) {
        currentqpage++;
        showqpage(currentqpage);
      }
    }
  
    // 初始显示第一页
    showqpage(currentqpage);

 function validateGrade() {
  var gradeInput = document.getElementById('grade');
  var grade = parseFloat(gradeInput.value);

  if (isNaN(grade) || grade < 0 || grade > 100) {
    gradeInput.setCustomValidity('Grade must be a number between 0 and 100.');
  } else {
    gradeInput.setCustomValidity('');
  }
}
function hideAlert(alertElement) {
    alertElement.classList.add('fade-out');
    setTimeout(function() {
        alertElement.style.display = 'none';
    }, 50); // wait CSS
}

window.onload = function() {
    var alertElement = document.querySelector('.warning-alert');
    setTimeout(function() {
        hideAlert(alertElement);
    }, 2000); // hideAlert function after 2 second
}