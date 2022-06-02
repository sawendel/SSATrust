import { Fragment } from 'react';
import { Container, Row, Col } from 'react-bootstrap';
import Tooltip from '../../../Tooltip';

const EmailHeaderDetails = ({ logEvent, config, date, showTooltips }) => {
  const details = [
    { label: 'From', value: `${config?.fromName}` === '' ? `${config?.fromEmail}` : `${config?.fromName} | ${config?.fromEmail}`, tooltipText: config?.fromTooltip },
    { label: 'Reply to', value: config?.replyTo, tooltipText: config?.replyToTooltip },
    { label: 'To', value: config?.to, tooltipText: config?.toTooltip },
    { label: 'Date', value: date },
    { label: 'Mailed by', value: config?.mailedBy, tooltipText: config?.mailedByTooltip },
    { label: <i className="et-lock" />, value: 'Standard Encryption' },
  ];

  return (
    <Container fluid className="et-email-header-details">
      <Row>
        {details.map((x) => (
          <Fragment key={x.label}>
            <Col lg={3} xs={4} className="pb-2"><small className="text-lynch">{x.label}</small></Col>
            <Col lg={9} xs={8} className="pb-2">
              <Tooltip text={x.tooltipText} show={showTooltips}>
                <small>{x.value}</small>
              </Tooltip>
            </Col>
          </Fragment>
        ))}
      </Row>
    </Container>
  );
};

export default EmailHeaderDetails;
