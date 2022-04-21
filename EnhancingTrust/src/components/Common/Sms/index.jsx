import { useState } from 'react';
import moment from 'moment';
import TemplateRenderer from '../TemplateRenderer';

const Sms = (props) => {
  const [config, setConfig] = useState();
  const currentTime = moment().format('h:mm a');
  const { senderName = '', senderNumber = '' } = config || {};

  return (
    <div className="d-flex justify-content-center py-5">
      <div className="et-sms">
        <div className="et-sms__img d-none d-sm-block"></div>
        <div className="et-sms__header px-11 py-12 pt-sm-5">
          <i className='me-2 et-caret-left' />
          <div className="et-sms__avatar">
            <img alt="avatar" src={`https://ui-avatars.com/api/?name=${senderName}&background=03269E&color=fff&rounded=true&size=35`}></img>
            <h6>
              {senderName}
            </h6>
            <span>{senderNumber}</span>
          </div>
          <i className='me-2 et-info-circle' />
        </div>
        <div className="et-sms__content p-11 px-sm-13">
          <span className="pt-2"> Today • {currentTime}</span>
          <div className="et-sms__bubble pb-1">
            <TemplateRenderer {...props} setOptions={setConfig} />
          </div>
        </div>
        <div className="et-sms__footer py-12 px-13" >
          <i className='me-2 et-camera et-sms__footer__icon' />
          <i className='me-2 et-image-upload' />
          <input type="text" placeholder='Text message' />
          <i className='me-2 et-face-happy et-sms__footer__iconText' />
          <i className='et-mic et-sms__footer__iconText' />
        </div>
      </div>
    </div>
  );
};

export default Sms;
