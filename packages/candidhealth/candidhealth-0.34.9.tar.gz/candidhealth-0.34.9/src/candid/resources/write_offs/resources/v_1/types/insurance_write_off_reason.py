# This file was auto-generated by Fern from our API Definition.

import enum
import typing

T_Result = typing.TypeVar("T_Result")


class InsuranceWriteOffReason(str, enum.Enum):
    SMALL_BALANCE = "SMALL_BALANCE"
    NO_AUTHORIZATION_REFERRAL = "NO_AUTHORIZATION_REFERRAL"
    TIMELY_FILING = "TIMELY_FILING"
    STALE_DATE = "STALE_DATE"
    TIMELY_FILING_LATE_ENCOUNTER = "TIMELY_FILING_LATE_ENCOUNTER"
    CREDENTIALING_OR_CONTRACTING = "CREDENTIALING_OR_CONTRACTING"
    NON_COVERED_MAX_BENEFIT = "NON_COVERED_MAX_BENEFIT"
    NOT_MEDICALLY_NECESSARY = "NOT_MEDICALLY_NECESSARY"
    BUNDLED_OR_INCLUSIVE = "BUNDLED_OR_INCLUSIVE"
    UNCOLLECTIBLE_OR_NON_BILLABLE = "UNCOLLECTIBLE_OR_NON_BILLABLE"
    EFFORTS_EXHAUSTED = "EFFORTS_EXHAUSTED"
    ADMINISTRATIVE_WRITE_OFF = "ADMINISTRATIVE_WRITE_OFF"
    CASE_RATE_OR_CAPITATED = "CASE_RATE_OR_CAPITATED"
    OTHER = "OTHER"
    UNKNOWN = "UNKNOWN"
    CONTRACTUAL_ADJUSTMENT = "CONTRACTUAL_ADJUSTMENT"

    def visit(
        self,
        small_balance: typing.Callable[[], T_Result],
        no_authorization_referral: typing.Callable[[], T_Result],
        timely_filing: typing.Callable[[], T_Result],
        stale_date: typing.Callable[[], T_Result],
        timely_filing_late_encounter: typing.Callable[[], T_Result],
        credentialing_or_contracting: typing.Callable[[], T_Result],
        non_covered_max_benefit: typing.Callable[[], T_Result],
        not_medically_necessary: typing.Callable[[], T_Result],
        bundled_or_inclusive: typing.Callable[[], T_Result],
        uncollectible_or_non_billable: typing.Callable[[], T_Result],
        efforts_exhausted: typing.Callable[[], T_Result],
        administrative_write_off: typing.Callable[[], T_Result],
        case_rate_or_capitated: typing.Callable[[], T_Result],
        other: typing.Callable[[], T_Result],
        unknown: typing.Callable[[], T_Result],
        contractual_adjustment: typing.Callable[[], T_Result],
    ) -> T_Result:
        if self is InsuranceWriteOffReason.SMALL_BALANCE:
            return small_balance()
        if self is InsuranceWriteOffReason.NO_AUTHORIZATION_REFERRAL:
            return no_authorization_referral()
        if self is InsuranceWriteOffReason.TIMELY_FILING:
            return timely_filing()
        if self is InsuranceWriteOffReason.STALE_DATE:
            return stale_date()
        if self is InsuranceWriteOffReason.TIMELY_FILING_LATE_ENCOUNTER:
            return timely_filing_late_encounter()
        if self is InsuranceWriteOffReason.CREDENTIALING_OR_CONTRACTING:
            return credentialing_or_contracting()
        if self is InsuranceWriteOffReason.NON_COVERED_MAX_BENEFIT:
            return non_covered_max_benefit()
        if self is InsuranceWriteOffReason.NOT_MEDICALLY_NECESSARY:
            return not_medically_necessary()
        if self is InsuranceWriteOffReason.BUNDLED_OR_INCLUSIVE:
            return bundled_or_inclusive()
        if self is InsuranceWriteOffReason.UNCOLLECTIBLE_OR_NON_BILLABLE:
            return uncollectible_or_non_billable()
        if self is InsuranceWriteOffReason.EFFORTS_EXHAUSTED:
            return efforts_exhausted()
        if self is InsuranceWriteOffReason.ADMINISTRATIVE_WRITE_OFF:
            return administrative_write_off()
        if self is InsuranceWriteOffReason.CASE_RATE_OR_CAPITATED:
            return case_rate_or_capitated()
        if self is InsuranceWriteOffReason.OTHER:
            return other()
        if self is InsuranceWriteOffReason.UNKNOWN:
            return unknown()
        if self is InsuranceWriteOffReason.CONTRACTUAL_ADJUSTMENT:
            return contractual_adjustment()
