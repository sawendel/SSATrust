import { useEffect, useState } from 'react';
import PropTypes from 'prop-types' ;
import { Row, Col, Button } from 'react-bootstrap';
import moment from 'moment';
import Details from './Details';
import Tooltip from '../../Tooltip';

const EmailHeader = ({ config, showTooltips }) => {
  const [displayDetails, setDisplayDetails] = useState(false);
  const [displayTooltips, setDisplayTooltips] = useState(false);
  const currentDate = moment().subtract(2, 'days').format('MMMM Do, H:MM');
  const dateElement = (className = 'd-none d-lg-block') => <small className={`${className} text-lynch`}>{currentDate} (2 days ago)</small>;

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
      <Details config={config} date={currentDate} showTooltips={displayTooltips} />
    </div>
  );

  return config ? (
    <div className="et-email-header">
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
                  {config.fromName}  {dateElement('d-lg-none d-block fw-normal pt-2')}
                </p>
                <small className="text-lynch">
                  to: me
                  <Button
                    variant="link"
                    className={`et-email-header__expander ${displayDetails ? 'et-email-header__expander--active' : ''}`}
                    onClick={() => setDisplayDetails(!displayDetails)}
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
          <div className="d-flex justify-content-end et-email-header__actions">
            <small className="d-none d-lg-block text-lynch">{dateElement()}</small>
            <i className="et-response" />
            <i className="d-none d-lg-block et-reply-all" />
            <i className="d-none d-lg-block et-forward" />
            <i className="et-dots" />
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
    fromName: PropTypes.string.isRequired,
    to: PropTypes.string.isRequired,
    mailedBy: PropTypes.string.isRequired,
  }),
};

export default EmailHeader;
