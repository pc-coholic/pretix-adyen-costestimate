'use strict';

var pretixadyen = {
    adyen: null,

    'load': async function () {
        pretixadyen.adyen = await AdyenCheckout({
            locale: $.trim($("body").attr("data-locale")),
            environment: $.trim($("#adyen_environment").html()),
            clientKey: $.trim($("#adyen_clientKey").html()),

            onChange: function (state, component) {
                if (state.isValid) {
                    $("#encrypted_carddata").val(JSON.stringify(state.data.paymentMethod.encryptedCardNumber));
                    $('#encrypted_carddata').closest("form").get(0).submit();
                } else {
                    $("#encrypted_carddata").val('');
                }
            },
            onError: function (error) {
                console.log("onError", error);
            },
        });

        pretixadyen.adyen.create('card', {
            hasHolderName: false,
            holderNameRequired: false,
            hideCVC: true,
            expiryDateRequired: false
        }).mount("#card-container");
    },
};


$(function () {
    pretixadyen.load();
});

