import { useEffect, useState } from 'react';
import PropTypes from 'prop-types';
import { Row, Col, Button } from 'react-bootstrap';
import moment from 'moment';
import Details from './Details';
import Tooltip from '../../Tooltip';
import { Events } from '../../../../constants';
import Overlay from '../../Overlay';
import { toast } from 'react-toastify';

const EmailHeader = ({ logEvent, config, showTooltips }) => {
  const [displayDetails, setDisplayDetails] = useState(false);
  const [displayTooltips, setDisplayTooltips] = useState(false);
  const currentDate = moment().subtract(2, 'days').format('MMMM Do, H:MM');
  const date = (date) => {
    if (date) {
      return date;
    }
    else {
      return `${currentDate} (2 days ago)`;
    }
  }
  const dateElement = (className = 'd-none d-lg-block') => <small className={`${className} text-lynch`}>{date(config.date)} </small>;

  const [showOverlay, setShowOverlay] = useState(false);


  const eventHandler = (e, event, attribs, metadata) => {
    if (typeof attribs?.['data-default'] === 'undefined') {
      e.preventDefault();
      e.stopPropagation();
    }

    logEvent(event, metadata);
  };

  const onLinkClick = (...params) => {
    eventHandler(...params);
    toast.info("All links have been disabled in this study", {
      onClose: () => setShowOverlay(false),
      onOpen: () => setShowOverlay(true),
    });
    toast.clearWaitingQueue();
  }

  useEffect(() => {
    if (showTooltips && (
      config?.fromTooltip || config?.replyToTooltip || config?.toTooltip || config?.mailedByTooltip
    )) {
      setDisplayDetails(showTooltips);
      setTimeout(() => setDisplayTooltips(showTooltips), 300);
    } else if (!showTooltips) {
      setDisplayDetails(false);
      setDisplayTooltips(false);
    }
  }, [showTooltips]);

  const buildDetails = (isForMobile = false) => (
    <div className={`et-email-header__details ${isForMobile ? 'd-block d-sm-none' : 'd-none d-sm-block'} ${!displayDetails ? 'et-email-header__details--hidden' : ''}`}>
      <Details logEvent={logEvent} config={config} date={currentDate} showTooltips={displayTooltips} />
    </div>
  );

  const onToggleDetails = () => {
    const event = displayDetails ? Events.EMAIL_DETAILS_COLLAPSED : Events.EMAIL_DETAILS_EXPANDED;
    setDisplayDetails(!displayDetails);
    logEvent(event);
  };

  const name = (fromName, fromEmail) => {
    if (fromName) {
      return fromName;
    }
    else {
      return fromEmail;
    }
  }

  return config ? (
    <div className="et-email-header">
      {showOverlay && <Overlay onClick={() => toast.dismiss()} />}
      <h4 className="fw-normal">
        <Tooltip text={config?.subjectTooltip} show={showTooltips}>
          <span>{config.subject}</span>
        </Tooltip>
      </h4>
      <Row>
        <Col lg={6} xs={8}>
          <Row>
            <Col xs="auto">
              <img src="/email_photo.png" alt="profile" width="48" height="48" />
            </Col>
            <Col>
              <div className="d-flex justify-content-center flex-column h-100">
                <p className="mb-1 fw-bold">
                  {name(config.fromName, config.fromEmail)} {dateElement('d-lg-none d-block fw-normal pt-2')}
                </p>
                <small className="text-lynch">
                  to: me
                  <Button
                    variant="link"
                    className={`et-email-header__expander ${displayDetails ? 'et-email-header__expander--active' : ''}`}
                    onClick={onToggleDetails}
                  >
                    <i className="et-caret-down" />
                  </Button>
                </small>
                {buildDetails()}
              </div>
            </Col>
          </Row>
        </Col>
        <Col lg={6} xs={4}>
          <div className="d-flex justify-content-end align-items-center et-email-header__actions">
            <small className="d-none d-lg-block text-lynch">{dateElement()}</small>
            <Button variant="link" className="et-email__icon-btn" onClick={(e) => onLinkClick(e, Events.EMAIL_REPLY)}>
              <i className="et-response" />
            </Button>
            <Button variant="link" className="d-none d-lg-block et-email__icon-btn" onClick={(e) => onLinkClick(e, Events.EMAIL_REPLY_ALL)}>
              <i className="et-reply-all" />
            </Button>
            <Button variant="link" className="d-none d-lg-block et-email__icon-btn" onClick={(e) => onLinkClick(e, Events.EMAIL_FORWARD)}>
              <i className="et-forward" />
            </Button>
          </div>
        </Col>
      </Row>
      {buildDetails(true)}
    </div>
  ) : null;
};

EmailHeader.propTypes = {
  config: PropTypes.shape({
    subject: PropTypes.string.isRequired,
    fromEmail: PropTypes.string.isRequired,
    to: PropTypes.string.isRequired,
    mailedBy: PropTypes.string.isRequired,
  }),
};

export default EmailHeader;
