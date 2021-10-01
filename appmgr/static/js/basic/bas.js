// Author: sphong1
// Filename: BASic


function bas_submit_page_no(a, page_no) {
  const oForm = $(a).parents("form").eq(0);
  const frm_id = oForm.attr("id");
  const oInput = oForm.find("input[name='page_no']");

  if (typeof oInput.val() == "undefined") {
    alert("ERR_bas: " + frm_id + ".page_no does not exist.");
    return;
  }

  oInput.val(page_no);
  bas_submit_form(frm_id);
}


function bas_submit_page_size(select) {
  const oForm = $(select).parents("form").eq(0);
  const frm_id = oForm.attr("id");
  oForm.find("input[name='page_no']").val("1");
  bas_submit_form(frm_id);
}


function bas_submit_page_sort(a, ordby_col_new) {
  const oForm = $(a).parents("form").eq(0);
  const frm_id = oForm.attr("id");
  const ordby_col_old = oForm.find("input[name='ordby_col']").val();

  if (typeof ordby_col_old == "undefined") {
    alert("ERR_bas: " + frm_id + ".ordby_col does not exist.");
    return;
  }

  let ordby_adc_old = oForm.find("input[name='ordby_adc']").val();

  if (typeof ordby_adc_old == "undefined") {
    alert("ERR_bas: " + frm_id + ".ordby_adc does not exist.");
    return;
  }

  ordby_adc_old = ordby_adc_old.toUpperCase();

  const ordby_adc_new = (ordby_col_old == ordby_col_new ? (ordby_adc_old == "DESC" ? "ASC" : "DESC") : "DESC");
  oForm.find("input[name='ordby_col']").val(ordby_col_new);
  oForm.find("input[name='ordby_adc']").val(ordby_adc_new);
  bas_submit_form(frm_id);
}


function bas_submit_form(frm_id) {
  if (frm_id == "") {
    alert("ERR_bas: form.id is empty.");
    return;
  }

  const oForm = $("#" + frm_id);
  const frm_div = oForm.find("input[name='frm_div']").val();

  if (typeof frm_div == "undefined") {
    oForm.submit();
    return;
  }

  if ($("#" + frm_div).length == 0) {
    alert("ERR_bas: " + frm_id + ".frm_div is invalid.");
    return;
  }

  const frm_mth = oForm.prop("method");
  const frm_url = oForm.attr("action");

  if (frm_url == "") {
    alert("ERR_bas: " + frm_id + ".action is empty.");
    return;
  }

  oForm.find("input[name='content_type']").val("");

  let frm_par = oForm.serialize();
  let frm_add = oForm.find("input[name='frm_add']").val();
  let ifr_frm;

  if (typeof frm_add == "string") {
    frm_add = frm_add.replace(/\s/g, "");

    if (frm_add != "") {
      const frm_adds = frm_add.split(",");
      for (let idx in frm_adds) {
        ifr_frm = frm_adds[idx].split(".");
        frm_par += (frm_par == "" ? "" : "&");

        if (ifr_frm.length == 2) {
          if (frames[ifr_frm[0]]) {
            frm_par += $("#" + ifr_frm[1], frames[ifr_frm[0]].document).serialize();
          }
        }
        else {
          frm_par += $("#" + ifr_frm[0]).serialize();
        }
      }
    }
  }

  if (frm_mth == "get") {
    bas_submit_get_div(frm_url, frm_par, frm_div);
  }
  else if (frm_mth == "post") {
    bas_submit_post_div(frm_url, frm_par, frm_div);
  }
}


function bas_submit_get_div(url, par, div, mode="") {
  bas_show_loading(div);

  $.get(url, par, function(data) {
    $("#" + div).html(data);
    bas_hide_loading(div);
    if (mode == "modal") {
      $("#" + div + " .modal").modal()
    }
  });
}


function bas_submit_post_div(url, par, div, mode="") {
  bas_show_loading(div);

  $.post(url, par, function(data) {
    $("#" + div).html(data);
    bas_hide_loading(div);
    if (mode == "modal") {
      $("#" + div + " .modal").modal()
    }
  });
}


function bas_submit_page_down(a, content_type) {
  const frm = $(a).parents("form")[0];

  if (frm.content_type) {
    frm.content_type.value = content_type;
  }
  else {
    alert("ERR_bas: " + frm.id + ".content_type does not exist.");
    return;
  }

  if (frm.frm_add) {
    let frm_add = frm.frm_add.value;
    frm_add = frm_add.replace(/\s/g, "");
    const frm_adds = frm_add.split(",");
    let ifr_frm, fields;
    for (let idx in frm_adds) {
      ifr_frm = frm_adds[idx].split(".");

      if (ifr_frm.length == 2) {
        if (frames[ifr_frm[0]]) {
          fields = $("#" + ifr_frm[1], frames[ifr_frm[0]].document).serializeArray();
        }
      }
      else {
        fields = $("#" + ifr_frm[0]).serializeArray();
      }

      $.each(fields, function(i, field) {
        if (field.name.match(/\[\]$/) && frm[field.name]) {
          const len = frm[field.name].length;

          if (len) {
            // It is important to remove the last element first.
            for (let i = len - 1; i >= 0; i --) {
              obj.parentNode.removeChild(frm[field.name][i]);
            }
          }
          else {
            frm.removeChild(frm[field.name]);
          }
        }
      });

      $.each(fields, function(i, field) {
        bas_set_form_hidden(frm, field.name, field.value);
      });
    }
  }

  frm.submit();
}


function bas_set_form_hidden(frm, name, value) {
  if (name.match(/\[\]$/)) {
    bas_append_form_hidden(frm, name, value);
  }
  else if (frm[name]) {
    frm[name].value = value;
  }
  else {
    bas_append_form_hidden(frm, name, value);
  }
}


function bas_append_form_hidden(frm, name, value) {
  const o = document.createElement("input");
  o.type = "hidden";
  o.name = name;
  o.value = value;

  frm.appendChild(o);
}


function bas_show_loading(div) {
  const loading = '<div class="text-center" id="' + div + '_loading"><i class="fas fa-spinner fa-spin"></i> Processing. Please wait.</div>';
  $("#" + div).css("opacity", "0.5").after(loading);
  $("#" + div + "_loading").show();
}


function bas_hide_loading(div) {
  $("#" + div).css("opacity", "1");
  $("#" + div + "_loading").remove();
}


function bas_set_chkall(frm_id, chk_all, chk_arr) {
  $(document).off("click", "#" + frm_id + " input[name=" + chk_all + "]");

  $(document).on("click", "#" + frm_id + " input[name=" + chk_all + "]", function() {
    $("#" + frm_id + " input[name^='" + chk_arr + "']:enabled").prop("checked", $(this).prop("checked"));
  });

  $(document).off("click", "#" + frm_id + " input[name^='" + chk_arr + "']");

  $(document).on("click", "#" + frm_id + " input[name^='" + chk_arr + "']", function() {
    $("#" + frm_id + " input[name=" + chk_all + "]").prop("checked",
      $("#" + frm_id + " input[name^='" + chk_arr + "']:enabled").length ==
      $("#" + frm_id + " input[name^='" + chk_arr + "']:checked").length
    );
  });
}


function bas_set_datepicker(selector) {
  $(selector).datepicker({
    changeMonth: true,
    changeYear: true,
    dateFormat: "yy-mm-dd",
    duration: ""
  });
}


function bas_trim(str) {
  return str.replace(/(^\s+|\s+$)/g, "");
}


function bas_open_div(div, d_left, d_top) {
  const oDiv = $("#" + div);

  if (typeof d_left == "undefined") {
    d_left = 0;
  }

  if (typeof d_top == "undefined") {
    d_top = 0;
  }

  const b_left = event.pageX + d_left;
  const b_top = event.pageY + d_top;
  const doc_width = $(document).width();
  const div_width = oDiv.outerWidth();
  let div_left;

  if (doc_width <= b_left + div_width) {
    if (div_width < b_left) {
      div_left = b_left - div_width;
    }
    else {
      div_left = $(window).scrollLeft() + Math.max(($(window).width() - div_width) / 2, 0);
    }
  }
  else {
    div_left = b_left;
  }

  const doc_height = $(document).height();
  const div_height = oDiv.outerHeight();
  let div_top;

  if (doc_height <= b_top + div_height) {
    const foo_height = $("#footer").outerHeight() + 20;

    if (doc_height > div_height + foo_height) {
      div_top = doc_height - div_height - foo_height;
    }
    else {
      div_top = $(window).scrollTop() + Math.max(($(window).height() - div_height) / 2, 0);
    }
  }
  else {
    div_top = b_top;
  }

  oDiv.css({"left":div_left, "top":div_top});
  oDiv.show();
}
