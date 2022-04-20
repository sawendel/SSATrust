import { useState, useMemo } from 'react';
import moment from 'moment';
import TemplateRenderer from '../TemplateRenderer';

const Letter = (props) => {
  const [config, setConfig] = useState();
  const date = useMemo(() => moment().subtract(2, 'days').format('MMMM Do, YYYY'), []);

  return (
    <div className="d-flex justify-content-center pt-5">
      <div className='et-letter px-4 py-3 px-md-13 py-md-11'>
        <div className='et-letter__header__up'>
          <div className='et-letter__header__logo'>
            <img alt="company logo" src={config?.companyInfo?.logo} />
            <span className='p-2 px-md-2 pt-md-4'>{config?.companyInfo?.name}</span>
          </div>
          <div className='et-letter__header__slogan p-2 px-md-2 pt-md-4'>
            {config?.companyInfo?.slogan}
          </div>
        </div>

        <div className='et-letter__header__separator pt-2'></div>

        <div className='et-letter__header__down'>
          <div className='et-letter__header__companyName py-2 px-1'>
            <span className='et-letter__header__tittle'>{config?.companyInfo?.name}</span>
            <span>{config?.companyInfo?.streetAddress}</span>
            <span>{config?.companyInfo?.addressLine}</span>
            <span>{config?.companyInfo?.country}</span>
          </div>
          <div className='et-letter__header__recipientName py-2 px-13 px-md-15 px-lg-13'>
            <span className='et-letter__header__tittle'>{config?.recipientInfo?.name}</span>
            <span>{config?.recipientInfo?.title}</span>
            <span>{config?.recipientInfo?.streetAddress}</span>
            <span>{config?.recipientInfo?.addressLine}</span>
          </div>
        </div>

        <div className='et-letter__content px-1'>
          <div className='et-letter__content__date'>
            <span>{config?.salutation}</span>
            <span>{date}</span>
          </div>
          <div className='et-letter__content__text py-2'>
            <TemplateRenderer {...props} setOptions={setConfig} />
          </div>
          <div className='et-letter__content__footer'>
            <div className='et-letter__sender'>
              <span>{config?.senderInfo?.name}</span>
              <span>{config?.senderInfo?.title}</span>
            </div>
            <div className='et-letter__contact px-4'>
              <span>Contact info:</span>
              <span>Phone: {config?.contactInfo?.phone}</span>
              <span>Mail: {config?.contactInfo?.email}</span>
            </div>
          </div>
        </div>

        <div className='et-letter__final px-15 py-4'>
          <p>
            {config?.footer}
          </p>
        </div>
      </div>
    </div>
  );
};

export default Letter;
