import PropTypes from 'prop-types' ;
import { Row, Col } from 'react-bootstrap';
import moment from 'moment';

const EmailHeader = ({ config }) => {
  const currentDate = moment().subtract(2, 'days').format('MMMM Do, H:MM');
  const dateElement = (className = 'd-none d-lg-block') => <small className={`${className} text-lynch`}>{currentDate} (2 days ago)</small>;

  return config ? (
    <div className="et-email-header">
      <h4 className="fw-normal">{config.subject}</h4>
      <Row>
        <Col xs="auto">
          <Row>
            <Col xs="auto">
              <img src="/email_photo.png" alt="profile" width="48" height="48" />
            </Col>
            <Col>
              <div className="d-flex justify-content-center flex-column h-100">
                <p className="mb-1 fw-bold">
                  {config.fromName}  {dateElement('d-lg-none d-block fw-normal')}
                </p>
                <small className="text-lynch">to: me</small>
              </div>
            </Col>
          </Row>
        </Col>
        <Col>
          <div className="d-flex justify-content-end et-email-header__actions">
            <small className="d-none d-lg-block text-lynch">{dateElement()}</small>
            <i className="et-response" />
            <i className="d-none d-lg-block et-reply-all" />
            <i className="d-none d-lg-block et-forward" />
            <i className="et-dots" />
          </div>
        </Col>
      </Row>
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
