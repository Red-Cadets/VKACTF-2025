package auth

import (
	"css/internal/models"
	"encoding/hex"
	"fmt"
	"strings"
	"time"

	"golang.org/x/crypto/sha3"
)

func GenerateAtomID(user *models.User) string {

	return addChecksum(formatAtomID(hashWithSHA3(addTimestampEntropy(combineUserData(*user)))))
}

func combineUserData(user models.User) string {
	return fmt.Sprintf(
		"%s|%s|%s|%d|%s",
		user.Username,
		user.Email,
		user.Number,
		user.ID,
		user.CreatedAt.Format("20060102150405"),
	)
}

func addTimestampEntropy(input string) string {
	return fmt.Sprintf("%s|%d", input, time.Now().UnixNano())
}

func hashWithSHA3(input string) string {
	h := sha3.New256()
	h.Write([]byte(input))
	return hex.EncodeToString(h.Sum(nil))
}

func formatAtomID(hash string) string {
	if len(hash) < 28 {
		hash = hash + strings.Repeat("0", 28-len(hash))
	}
	return fmt.Sprintf(
		"ATOM-%s-%s-%s-%s",
		hash[0:4],
		hash[4:8],
		hash[8:12],
		hash[12:24],
	)
}

func addChecksum(id string) string {
	sum := 0
	for _, r := range id {
		sum += int(r)
	}
	checksumChar := rune('A' + (sum % 26))
	return fmt.Sprintf("%s-%c", id, checksumChar)
}
