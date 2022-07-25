import { useState, useMemo } from 'react';
import moment from 'moment';
import TemplateRenderer from '../TemplateRenderer';
import Tooltip from '../Tooltip';

const Letter = (props) => {
  const [config, setConfig] = useState();
  const date = useMemo(() => moment().subtract(2, 'days').format('MMMM Do, YYYY'), []);

  return (
    <div className="d-flex justify-content-center py-5">
      <div className='et-letter px-4 py-3 px-md-13 py-md-11'>
        <div className='et-letter__header__up'>
          <div className='et-letter__header__logo'>
            <Tooltip show={props.showTooltips} text={config?.companyInfo?.logoTooltip}>
              <img alt="company logo" src={config?.companyInfo?.logo} />
            </Tooltip>
            <Tooltip show={props.showTooltips} text={config?.companyInfo?.sloganTooltip} placement="right">
              <span className='p-2 px-md-2 pt-md-4'>{config?.companyInfo?.slogan}</span>
            </Tooltip>
          </div>
        </div>

        <div className='et-letter__header__separator pt-2'></div>

        <div className='et-letter__header__down py-md-1'>
        </div>

        <div className='et-letter__content px-1'>
          <div className='et-letter__content__text py-2'>
            <TemplateRenderer {...props} setOptions={setConfig} />
          </div>
          <div className='et-letter__content__footer py-md-3'>
            <div className='et-letter__sender'>
              <Tooltip show={props.showTooltips} text={config?.senderInfo?.nameTooltip}>
                <span>{config?.senderInfo?.name}</span>
              </Tooltip>
              <Tooltip show={props.showTooltips} text={config?.senderInfo?.titleTooltip} placement="bottom">
                <span>{config?.senderInfo?.title}</span>
              </Tooltip>
            </div>
          </div>
        </div>

        <div className='et-letter__final px-15 py-4 py-lg-1'>
          <p>
            <Tooltip show={props.showTooltips} text={config?.footerTooltip}>
              <span>{config?.footer}</span>
            </Tooltip>
          </p>
        </div>
      </div>
    </div>
  );
};

export default Letter;
